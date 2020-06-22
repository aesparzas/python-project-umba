import datetime
import json
import statistics

import numpy as np
import pytest
import sqlite3
import time
import unittest

from app import app

class SensorRoutesTestCases(unittest.TestCase):

    def setUp(self):
        # Setup the SQLite DB
        conn = sqlite3.connect('test_database.db')
        conn.execute('DROP TABLE IF EXISTS readings')
        conn.execute('CREATE TABLE IF NOT EXISTS readings (device_uuid TEXT, type TEXT, value INTEGER, date_created INTEGER)')
        
        self.device_uuid = 'test_device'

        # Setup some sensor data
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute('insert into readings (device_uuid,type,value,date_created) VALUES (?,?,?,?)',
                    (self.device_uuid, 'temperature', 22, int(time.time()) - 100))
        cur.execute('insert into readings (device_uuid,type,value,date_created) VALUES (?,?,?,?)',
                    (self.device_uuid, 'temperature', 50, int(time.time()) - 50))
        cur.execute('insert into readings (device_uuid,type,value,date_created) VALUES (?,?,?,?)',
                    (self.device_uuid, 'temperature', 100, int(time.time())))

        cur.execute('insert into readings (device_uuid,type,value,date_created) VALUES (?,?,?,?)',
                    ('other_uuid', 'temperature', 22, int(time.time())))
        conn.commit()

        app.config['TESTING'] = True

        self.client = app.test_client

    def test_device_readings_get(self):
        # Given a device UUID
        # When we make a request with the given UUID
        request = self.client().get(f'/devices/{self.device_uuid}/readings')

        # Then we should receive a 200
        self.assertEqual(request.status_code, 200)

        # And the response data should have three sensor readings
        self.assertTrue(len(json.loads(request.data)) == 3)

    def test_device_readings_post(self):
        # Given a device UUID
        # When we make a request with the given UUID to create a reading
        data = {
            'type': 'temperature',
            'value': 100
        }
        request = self.client().post(f'/devices/{self.device_uuid}/readings',
                                     data=json.dumps(data))

        # Then we should receive a 201
        self.assertEqual(request.status_code, 201)

        # And when we check for readings in the db
        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'select * from readings where device_uuid="{self.device_uuid}"'
        )
        rows = cur.fetchall()

        # We should have three
        self.assertTrue(len(rows) == 4)

    def test_device_readings_get_temperature(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's temperature data only.
        """
        url = f'/devices/{self.device_uuid}/readings?type=temperature'
        request = self.client().get(url)
        self.assertEqual(request.status_code, 200)
        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'''select * from readings where device_uuid="{self.device_uuid}"
            and type="temperature"'''
        )
        rows = cur.fetchall()
        self.assertEqual(len(rows), len(json.loads(request.data)))

    def test_device_readings_get_humidity(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's humidity data only.
        """
        url = f'/devices/{self.device_uuid}/readings?type=temperature'
        request = self.client().get(url)
        self.assertEqual(request.status_code, 200)
        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'''select * from readings where device_uuid="{self.device_uuid}"
            and type="temperature"'''
        )
        rows = cur.fetchall()
        self.assertEqual(len(rows), len(json.loads(request.data)))

    def test_device_readings_get_past_dates(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's sensor data over
        a specific date range. We should only get the readings
        that were created in this time range.
        """

        from_date = int(time.time()) - 100
        prev_date = (datetime.datetime.fromtimestamp(from_date).date()
                     - datetime.timedelta(days=1))
        fd_isoformat = prev_date.isoformat()
        from_date = int(time.mktime(prev_date.timetuple()))

        to_date = int(time.time()) - 50
        prev_date = (datetime.datetime.fromtimestamp(to_date).date()
                     - datetime.timedelta(days=1))
        td_isoformat = prev_date.isoformat()
        to_date = int(time.mktime(prev_date.timetuple()))

        url = f'/devices/{self.device_uuid}/readings'\
              + f'?date_to={td_isoformat}'\
              + f'&date_from={fd_isoformat}'
        request = self.client().get(url)
        self.assertEqual(request.status_code, 200)
        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'''select * from readings where device_uuid="{self.device_uuid}"
            and date_created < {to_date} and date_created > {from_date}'''
        )
        rows = cur.fetchall()
        self.assertEqual(len(rows), len(json.loads(request.data)), f'{from_date} {to_date}')

    def test_device_readings_min(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's min sensor reading.
        """
        url = f'/devices/{self.device_uuid}/readings/min'
        request = self.client().get(url)
        self.assertEqual(request.status_code, 200)
        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'select * from readings where device_uuid="{self.device_uuid}"'
        )
        rows = cur.fetchall()
        values = [r['value'] for r in rows]
        self.assertEqual(min(values), json.loads(request.data)['value'])

    def test_device_readings_max(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's max sensor reading.
        """
        url = f'/devices/{self.device_uuid}/readings/max'
        request = self.client().get(url)
        self.assertEqual(request.status_code, 200)
        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'select * from readings where device_uuid="{self.device_uuid}"'
        )
        rows = cur.fetchall()
        values = [r['value'] for r in rows]
        self.assertEqual(max(values), json.loads(request.data)['value'])

    def test_device_readings_median(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's median sensor reading.
        """
        url = f'/devices/{self.device_uuid}/readings/median'
        request = self.client().get(url)
        self.assertEqual(request.status_code, 200)
        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'select * from readings where device_uuid="{self.device_uuid}"'
        )
        rows = cur.fetchall()
        values = [r['value'] for r in rows]
        self.assertEqual(statistics.median(values),
                         json.loads(request.data)['value'])

    def test_device_readings_mean(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's mean sensor reading value.
        """
        url = f'/devices/{self.device_uuid}/readings/mean'
        request = self.client().get(url)
        self.assertEqual(request.status_code, 200)
        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'select * from readings where device_uuid="{self.device_uuid}"'
        )
        rows = cur.fetchall()
        values = [r['value'] for r in rows]
        self.assertEqual(statistics.mean(values),
                         json.loads(request.data)['value'])

    def test_device_readings_mode(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's mode sensor reading value.
        """
        url = f'/devices/{self.device_uuid}/readings/mode'
        request = self.client().get(url)
        self.assertEqual(request.status_code, 200)
        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'select * from readings where device_uuid="{self.device_uuid}"'
        )
        rows = cur.fetchall()
        values = [r['value'] for r in rows]
        try:
            self.assertEqual(statistics.mode(values),
                             json.loads(request.data)['value'])
        except statistics.StatisticsError:
            self.assertEqual("Multiple Modes",
                             json.loads(request.data)['value'])

    def test_device_readings_quartiles(self):
        """
        This test should be implemented. The goal is to test that
        we are able to query for a device's 1st and 3rd quartile
        sensor reading value.
        """
        url = f'/devices/{self.device_uuid}/readings/quartiles'
        request = self.client().get(url)
        self.assertEqual(request.status_code, 200)
        json_data = json.loads(request.data)

        conn = sqlite3.connect('test_database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f'select * from readings where device_uuid="{self.device_uuid}"'
        )
        rows = cur.fetchall()
        values = [r['value'] for r in rows]
        quartile_1 = np.percentile(values, 25)
        quartile_3 = np.percentile(values, 75)

        self.assertEqual(quartile_1, json_data['quartile_1'])
        self.assertEqual(quartile_3, json_data['quartile_3'])
