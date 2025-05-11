CREATE TABLE IF NOT EXISTS iot_data (
  device_id VARCHAR(256),
  temperature FLOAT,
  humidity FLOAT,
  event_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS error_log (
  device_id VARCHAR(256),
  error_message VARCHAR(512),
  event_timestamp TIMESTAMP
);