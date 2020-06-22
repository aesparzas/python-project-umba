from marshmallow import Schema, fields, validate


class ReadingSerializer(Schema):
    type = fields.String(required=True,
                         validate=validate.OneOf(["temperature", "humidity"]))
    device_uuid = fields.String(required=True)
    value = fields.Number(required=True,
                          validate=validate.Range(min=0, max=100))
    date_created = fields.Date()


class QueryReadingsSerializer(Schema):
    type = fields.String()
    date_from = fields.Date()
    date_to = fields.Date()
