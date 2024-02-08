import base64
from flask import Flask
from flask import request, jsonify
import os
from message_pb2 import Message, Empty, PushStatus
import grpc
import message_pb2_grpc
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

channel = grpc.insecure_channel(f"{os.getenv('ZOOKEEPER_HOST')}:{os.getenv('ZOOKEEPER_PORT')}")
stub = message_pb2_grpc.MessageQueueStub(channel)

app = Flask(__name__)


@app.route("/push", methods=["POST"])
def push():
    key = request.form["key"]
    value = base64.b64decode(request.form["value"])
    logger.info(f"Pushing message: {key} {value}")
    message = Message(key=key, value=value)
    response = stub.Push(message)
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
    response = stub.Pull(Empty())
    logger.info(f"Pulled message: {response.key} {response.value}")
    value = response.value
    value = base64.b64encode(value).decode("utf-8")
    logger.debug(f"Returning message: {response.key} {value}")
    return jsonify(
        key=response.key,
        value=value,
    )