"""Consumes price ticks and records every sequence number it processes to /data/consumed.jsonl.

COMMIT_MODE controls when the offset is committed relative to "processing" (writing the line):
  before_process : commit, then process  → a crash in between LOSES messages (at-most-once)
  after_process  : process, then commit  → a crash in between DUPLICATES messages (at-least-once)
  auto           : the client commits on a timer, independent of processing
"""
import json
import os
import time

from confluent_kafka import Consumer

mode = os.getenv("COMMIT_MODE", "after_process")
process_ms = float(os.getenv("PROCESS_MS", "0"))

consumer = Consumer({
    "bootstrap.servers": os.environ["BOOTSTRAP"],
    "group.id": os.getenv("GROUP_ID", "order-router"),
    "auto.offset.reset": "earliest",
    "enable.auto.commit": mode == "auto",
})
consumer.subscribe([os.getenv("TOPIC", "price-ticks")])
out = open("/data/consumed.jsonl", "a", buffering=1)
print(f"consuming with COMMIT_MODE={mode} PROCESS_MS={process_ms}", flush=True)

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"consumer error: {msg.error()}", flush=True)
        continue
    if mode == "before_process":
        consumer.commit(message=msg, asynchronous=False)
    if process_ms:
        time.sleep(process_ms / 1000)
    value = json.loads(msg.value())
    out.write(json.dumps({"seq": value["seq"], "partition": msg.partition(), "offset": msg.offset(),
                          "latency_ms": round((time.time() - value["ts"]) * 1000, 1)}) + "\n")
    if mode == "after_process":
        consumer.commit(message=msg, asynchronous=False)
