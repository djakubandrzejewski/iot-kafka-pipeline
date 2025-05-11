from kafka import KafkaConsumer, KafkaProducer
from jsonschema import validate, ValidationError
import json
import time

# Wczytanie schematu
with open("validator/schema.json") as f:
    schema = json.load(f)

# Kafka consumer/producer
consumer = KafkaConsumer(
    "raw_iot",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="validator-group",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Plik logów
error_log = open("validator/error_log.txt", "a")

def is_valid_data(data):
    try:
        validate(instance=data, schema=schema)
        if not (0 <= data["temperature"] <= 50):
            raise ValueError("Temperature out of range")
        if not (0 <= data["humidity"] <= 100):
            raise ValueError("Humidity out of range")
        return True, None
    except (ValidationError, ValueError) as e:
        return False, str(e)

print("🛡️  Walidator uruchomiony...")

for msg in consumer:
    data = msg.value
    valid, error = is_valid_data(data)
    if valid:
        print(f"✅ OK: {data}")
        producer.send("iot_data", value=data)
    else:
        print(f"❌ Błąd: {data['device_id']} - {error}")
        error_log.write(f"{data['device_id']} - {error}\n")
        error_msg = {
            "device_id": data.get("device_id", "unknown"),
            "error_message": error,
            "event_timestamp": data.get("event_timestamp", int(time.time() * 1000))
        }
        producer.send("error_info", value=error_msg)

# nigdy się nie zamknie, ale w razie czego:
# error_log.close()