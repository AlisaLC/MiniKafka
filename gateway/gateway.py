import flask
from flask import request, Response
import os
from message_pb2 import Message, Empty, PushResponse
import grpc
import message_pb2_grpc

app = flask.Flask(__name__)


@app.route("/push", methods=["POST"])
def push():
    key = flask.request.form["key"]
    value = flask.request.form["value"]
    message = Message(key=key, value=value)
    response = stub.Push(message)
    if response.status == PushResponse.Status.OK:
        return Response({
            "message": response.message
        }, status=200)
    else:
        return Response({
            "message": response.message
        }, status=500)


@app.route("/pull", methods=["GET"])
def pull():
    key = request.args.get("key")
    response = stub.Pull(Empty())
    return Response({
        "key": response.key,
        "value": response.value
    })


if __name__ == "__main__":
    channel = grpc.insecure_channel(f"{os.getenv('ZOOKEEPER_HOST')}:{os.getenv('ZOOKEEPER_PORT')}")
    stub = message_pb2_grpc.MessageQueueStub(channel)
    app.run(host=os.getenv("GATEWAY_HOST"), port=os.getenv("GATEWAY_PORT"))
