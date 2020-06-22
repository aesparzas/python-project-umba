from marshmallow import Schema, fields


class ReadingSerializer(Schema):
    type = fields.String(required=True)
    device_uuid = fields.String(required=True)
    value = fields.Number(required=True)
    date_created = fields.Date()


class QueryReadingsSerializer(Schema):
    type = fields.String()
    date_from = fields.Date()
    date_to = fields.Date()
