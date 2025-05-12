from kafka import KafkaConsumer
import psycopg2
import json

# Konfiguracja połączenia z PostgreSQL
conn = psycopg2.connect(
    dbname="iot_db",
    user="iot_user",
    password="iot_pass",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Konsumenci
iot_consumer = KafkaConsumer(
    "iot_data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="processor-iot",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

error_consumer = KafkaConsumer(
    "error_info",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="processor-error",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("🧩 Processor uruchomiony...")

while True:
    iot_msgs = iot_consumer.poll(timeout_ms=1000)
    for tp, messages in iot_msgs.items():
        for msg in messages:
            d = msg.value
            print(f"📥 Zapisuję dane IoT: {d}")
            cursor.execute(
                "INSERT INTO iot_data (device_id, temperature, humidity, event_timestamp) VALUES (%s, %s, %s, to_timestamp(%s / 1000.0))",
                (d["device_id"], d["temperature"], d["humidity"], d["event_timestamp"])
            )
            conn.commit()

    error_msgs = error_consumer.poll(timeout_ms=1000)
    for tp, messages in error_msgs.items():
        for msg in messages:
            e = msg.value
            print(f"❗ Zapisuję błąd: {e}")
            cursor.execute(
                "INSERT INTO error_log (device_id, error_message, event_timestamp) VALUES (%s, %s, to_timestamp(%s / 1000.0))",
                (e["device_id"], e["error_message"], e["event_timestamp"])
            )
            conn.commit()
