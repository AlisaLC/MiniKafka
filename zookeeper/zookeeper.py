import grpc
from message_pb2 import Message, PushResponse, PushStatus
import message_pb2_grpc
import os
import time
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageQueue(message_pb2_grpc.MessageQueueServicer):
    def __init__(self):
        self.queue = []

    def Push(self, request, context):
        self.queue.append((request.key, request.value))
        logger.info(f"Pushed message: {request.key} {request.value}")
        return PushResponse(status=PushStatus.SUCCESS, message="")

    def Pull(self, request, context):
        logger.debug("Pulling message")
        while len(self.queue) == 0:
            time.sleep(1)
        message = self.queue.pop(0)
        logger.info(f"Pulled message: {message[0]} {message[1]}")
        return Message(key=message[0], value=message[1])
    
if __name__ == "__main__":
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessageQueueServicer_to_server(MessageQueue(), server)
    server.add_insecure_port(f"[::]:{os.getenv('ZOOKEEPER_PORT')}")
    server.start()
    server.wait_for_termination()
