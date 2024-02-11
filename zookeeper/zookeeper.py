import grpc
from proto.message_pb2 import PushResponse, Status, PullResponse, Message
import proto.message_pb2_grpc as message_pb2_grpc
from proto.zookeeper_pb2 import Empty
import proto.zookeeper_pb2_grpc as zookeeper_pb2_grpc

from broker import BrokerManager, Broker

import os
from concurrent.futures import ThreadPoolExecutor

from prometheus_client import start_http_server

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MessageQueue(message_pb2_grpc.MessageQueueServicer):
    def __init__(self, broker_manager: BrokerManager):
        self.broker_manager = broker_manager

    def Push(self, request, context):
        queue = self.broker_manager.get_node(request.key)
        if not queue:
            logger.error(f"No queue for key: {request.key}")
            return PushResponse(status=Status.FAILURE, message="No queue for key")
        response = queue.push(request.key, request.value)    
        logger.info(f"Pushed message: {request.key} {request.value}")
        return PushResponse(status=response.status, message=response.message)

    def Pull(self, request, context):
        queue = self.broker_manager.get_random_node()
        if not queue:
            logger.error("No brokers available")
            return PullResponse(status=Status.FAILURE, message=Message(key="", value=""))
        logger.debug(f"Pulling from queue: {queue.uuid}")
        response = queue.pull()
        message = response.message
        if response.status != Status.SUCCESS:
            logger.error(f"Failed to pull message")
            return PullResponse(status=Status.FAILURE, message=Message(key="", value=""))
        logger.debug(f"Pulled message: {message.key} {message.value}")
        return PullResponse(status=Status.SUCCESS, message=Message(key=message.key, value=message.value))

class Zookeeper(zookeeper_pb2_grpc.ZookeeperServicer):
    def __init__(self, broker_manager: BrokerManager):
        self.broker_manager = broker_manager

    def Ack(self, request, context):
        return Empty()
    
    def Register(self, request, context):
        logger.info(f"Registering broker: {request.uuid} {request.url}")
        self.broker_manager.add_node(Broker(request.uuid, request.url))
        return Empty()

    
if __name__ == "__main__":
    start_http_server(8000)
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    manager = BrokerManager()
    message_pb2_grpc.add_MessageQueueServicer_to_server(MessageQueue(manager), server)
    zookeeper_pb2_grpc.add_ZookeeperServicer_to_server(Zookeeper(manager), server)
    server.add_insecure_port(f"[::]:{os.getenv('ZOOKEEPER_PORT')}")
    server.start()
    server.wait_for_termination()
