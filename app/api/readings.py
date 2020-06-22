import sqlite3
import statistics
import time
from datetime import datetime, timedelta

from flask import request, jsonify
from marshmallow import ValidationError
import numpy as np

from app.api import api
from app.api.serializers import ReadingSerializer, QueryReadingsSerializer
from app.db import get_db


class DeviceView():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = get_db()

        self.get_sentence = '''
            SELECT date_created, device_uuid, type, value
            FROM readings
            WHERE device_uuid = "{}"
        '''

        self.POST_FIELDS = ['device_uuid', 'type', 'value']

        self.post_sentence = '''
            INSERT INTO readings (
                device_uuid,
                type,
                value,
                date_created
            )
            VALUES (?,?,?,?)
        '''

    def get_queried_data(self, device_uuid):
        valid_data = QueryReadingsSerializer().load(request.args)

        query = self.get_sentence.format(device_uuid)

        if 'type' in valid_data:
            query += ' AND type = "{}"'.format(valid_data['type'])

        if 'date_to' in valid_data:
            plus_day = valid_data['date_to'] + timedelta(days=1)
            ts = int(time.mktime(plus_day.timetuple()))
            query += ' AND date_created < {}'.format(ts)

        if 'date_from' in valid_data:
            plus_day = valid_data['date_from'] - timedelta(days=1)
            ts = int(time.mktime(plus_day.timetuple()))
            query += ' AND date_created > {}'.format(ts)

        cur = self.db.execute(query)
        rows = cur.fetchall()
        rows_dict = []

        for row in rows:
            row_dict = dict()
            for r in self.POST_FIELDS:
                row_dict[r] = row[r]
            row_dict['date_created'] = datetime.fromtimestamp(
                row['date_created'])
            rows_dict.append(row_dict)

        return ReadingSerializer(many=True).dump(rows_dict)


class RootDeviceView(DeviceView):
    def post(self, *args, **kwargs):
        data = request.get_json(force=True)
        if not data:
            return jsonify(dict(error="Body can't be empty")), 400
        data.update({
            'device_uuid': kwargs.get('uuid'),
        })
        valid_data = ReadingSerializer().load(data)

        model_data = [valid_data[e] for e in self.POST_FIELDS]
        model_data.append(int(time.time()))

        self.db.row_factory = sqlite3.Row
        cur = self.db.cursor()
        cur.execute(self.post_sentence, model_data)
        self.db.commit()

        return jsonify(dict(data=data)), 201

    def get(self, *args, **kwargs):
        return jsonify(self.get_queried_data(kwargs.get('uuid')))


class MetricsDeviceView(DeviceView):

    def _metric_to_query(self, uuid, func):
        queried = self.get_queried_data(uuid)
        value = None
        values = [r['value'] for r in queried]
        if values:
            value = func(values)
        return jsonify({'value': value})

    def max(self, *args, **kwargs):
        return self._metric_to_query(kwargs['uuid'], max)

    def min(self, *args, **kwargs):
        return self._metric_to_query(kwargs['uuid'], min)

    def quartiles(self, *args, **kwargs):
        queried = self.get_queried_data(kwargs.get('uuid'))
        quartile_1 = None
        quartile_3 = None
        values = [r['value'] for r in queried]
        if values:
            quartile_1 = np.percentile(values, 25)
            quartile_3 = np.percentile(values, 75)
        data = dict(quartile_1=quartile_1, quartile_3=quartile_3)
        return jsonify(data)

    def median(self, *args, **kwargs):
        return self._metric_to_query(kwargs['uuid'], statistics.median)
        pass

    def mean(self, *args, **kwargs):
        return self._metric_to_query(kwargs['uuid'], statistics.mean)

    def mode(self, *args, **kwargs):
        try:
            return self._metric_to_query(kwargs['uuid'], statistics.mode)
        except statistics.StatisticsError:
            return jsonify({"value": "Multiple Modes"})


@api.route('/devices/<uuid>/readings', endpoint='readings',
           methods=['POST', 'GET'])
def root_device(*args, **kwargs):
    view = RootDeviceView()
    method = getattr(view, request.method.lower())
    try:
        return method(*args, **kwargs)
    except ValidationError as e:
        return jsonify(str(e)), 400


@api.route('/devices/<uuid>/readings/<metrics>', methods=['POST', 'GET'])
def root_device(*args, **kwargs):
    view = MetricsDeviceView()
    try:
        method = getattr(view, kwargs.get('metrics'))
    except AttributeError:
        return jsonify('Not found'), 404
    try:
        return method(*args, **kwargs)
    except ValidationError as e:
        return jsonify(str(e)), 400
