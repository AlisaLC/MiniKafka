from flask import Flask
from flask import request, jsonify

from proto.message_pb2 import MQMessage, MQEmpty, MQStatus
import proto.message_pb2_grpc as message_pb2_grpc
import grpc

import base64
import os

import logging
from prometheus_client import generate_latest, Counter, Summary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PUSH_COUNTER = Counter("gateway_push_counter", "Number of push requests")
PULL_COUNTER = Counter("gateway_pull_counter", "Number of pull requests")
PUSH_LATENCY = Summary("gateway_push_latency", "Latency of push requests")
PULL_LATENCY = Summary("gateway_pull_latency", "Latency of pull requests")

channel = grpc.insecure_channel(f"{os.getenv('ZOOKEEPER_HOST')}:{os.getenv('ZOOKEEPER_PORT')}",
                                options=(('grpc.enable_http_proxy', 0),))


stub = message_pb2_grpc.MessageQueueStub(channel)

app = Flask(__name__)


@app.route("/push", methods=["POST"])
def push():
    key = request.form["key"]
    value = base64.b64decode(request.form["value"])
    logger.debug(f"Pushing message: {key} {value}")
    message = MQMessage(key=key, value=value)
    with PUSH_LATENCY.time():
        response = stub.Push(message)
    PUSH_COUNTER.inc()
    message = response.message
    if message == "":
        message = "No message"
    logger.debug(f"Push response: {'SUCCESS' if response.status == MQStatus.MQ_SUCCESS else 'FAILURE'} {message}")
    if response.status == MQStatus.MQ_SUCCESS:
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
        response = stub.Pull(MQEmpty())
    PULL_COUNTER.inc()
    if response.status != MQStatus.MQ_SUCCESS:
        logger.error(f"Failed to pull message")
        return jsonify(
            key="",
            value="",
        ), 500
    message = response.message
    logger.info(f"Pulled message: {message.key} {message.value}")
    value = message.value
    value = base64.b64encode(value).decode("utf-8")
    logger.debug(f"Returning message: {message.key} {value}")
    return jsonify(
        key=message.key,
        value=value,
    )


@app.route("/metrics", methods=["GET"])
def metrics():
    return generate_latest()
