from kafka import KafkaProducer
import json
import random
import time

# Konfiguracja Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Pętla wysyłająca dane
while True:
    message = {
        "device_id": f"sensor-{random.randint(1, 3)}",
        "temperature": round(random.uniform(-10, 60), 2),  # czasem błędne
        "humidity": round(random.uniform(-20, 120), 2),    # czasem błędne
        "event_timestamp": int(time.time() * 1000)         # timestamp w ms
    }

    print(f"Producent wysyła: {message}")
    producer.send("raw_iot", value=message)
    time.sleep(1)