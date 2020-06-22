DROP TABLE IF EXISTS readings;

CREATE TABLE IF NOT EXISTS readings(
    device_uuid TEXT,
    type TEXT,
    value INTEGER,
    date_created INTEGER
);