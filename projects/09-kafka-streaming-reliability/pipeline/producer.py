"""Publishes price ticks with a global sequence number.

Every message the broker ACKNOWLEDGES is appended to /data/produced.jsonl.
Comparing that file with /data/consumed.jsonl tells you exactly what was lost or duplicated.
"""
import json
import os
import random
import time

from confluent_kafka import Producer

INSTRUMENTS = ["AAPL", "MSFT", "ASML", "SHELL", "BTC-EUR", "ETH-EUR"]

conf = {
    "bootstrap.servers": os.environ["BOOTSTRAP"],
    "acks": os.getenv("ACKS", "all"),
    "enable.idempotence": os.getenv("ENABLE_IDEMPOTENCE", "true") == "true",
    "linger.ms": int(os.getenv("LINGER_MS", "5")),
}
if not conf["enable.idempotence"]:
    conf["retries"] = int(os.getenv("RETRIES", "2147483647"))

topic = os.getenv("TOPIC", "price-ticks")
rate = float(os.getenv("RATE", "200"))
producer = Producer(conf)
acked = open("/data/produced.jsonl", "a", buffering=1)


def on_delivery(err, msg):
    if err is None:
        acked.write(json.dumps({"seq": json.loads(msg.value())["seq"], "partition": msg.partition(),
                                "offset": msg.offset()}) + "\n")
    else:
        print(f"delivery failed: {err}", flush=True)


seq = 0
print(f"producing to {topic} at {rate}/s with {conf}", flush=True)
while True:
    instrument = random.choice(INSTRUMENTS)
    value = {"seq": seq, "instrument": instrument, "price": round(random.uniform(10, 500), 2), "ts": time.time()}
    while True:
        try:
            producer.produce(topic, key=instrument, value=json.dumps(value), on_delivery=on_delivery)
            break
        except BufferError:
            producer.poll(0.1)  # local queue full: wait for the brokers to catch up
    producer.poll(0)
    seq += 1
    time.sleep(1 / rate)
