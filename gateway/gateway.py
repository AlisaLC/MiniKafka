import base64
from flask import Flask
from flask import request, jsonify
import os
from message_pb2 import Message, Empty, PushStatus
import grpc
import message_pb2_grpc
import logging
from prometheus_client import generate_latest, Counter, Summary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

channel = grpc.insecure_channel(f"{os.getenv('ZOOKEEPER_HOST')}:{os.getenv('ZOOKEEPER_PORT')}")
stub = message_pb2_grpc.MessageQueueStub(channel)

app = Flask(__name__)

PUSH_COUNTER = Counter("gateway_push_counter", "Number of push requests")
PULL_COUNTER = Counter("gateway_pull_counter", "Number of pull requests")
PUSH_LATENCY = Summary("gateway_push_latency", "Latency of push requests")
PULL_LATENCY = Summary("gateway_pull_latency", "Latency of pull requests")

@app.route("/push", methods=["POST"])
def push():
    key = request.form["key"]
    value = base64.b64decode(request.form["value"])
    logger.info(f"Pushing message: {key} {value}")
    message = Message(key=key, value=value)
    with PUSH_LATENCY.time():
        response = stub.Push(message)
    PUSH_COUNTER.inc()
    message = response.message
    if message == "":
        message = "No message"
    logger.info(f"Push response: {response.status} {message}")
    if response.status == PushStatus.SUCCESS:
        return jsonify(
            message=message,
        )
    return jsonify(
        message=message,
    ), 500


@app.route("/pull", methods=["GET"])
def pull():
    logger.debug("Pulling message")
    with PULL_LATENCY.time():
        response = stub.Pull(Empty())
    PULL_COUNTER.inc()
    logger.info(f"Pulled message: {response.key} {response.value}")
    value = response.value
    value = base64.b64encode(value).decode("utf-8")
    logger.debug(f"Returning message: {response.key} {value}")
    return jsonify(
        key=response.key,
        value=value,
    )

@app.route("/metrics", methods=["GET"])
def metrics():
    return generate_latest()