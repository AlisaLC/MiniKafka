import grpc
from proto.message_pb2 import Message, PushResponse, PushStatus
import proto.message_pb2_grpc as message_pb2_grpc
from proto.zookeeper_pb2 import Empty
import proto.zookeeper_pb2_grpc as zookeeper_pb2_grpc

from broker import BrokerManager, Broker

import os
import time

from concurrent.futures import ThreadPoolExecutor

import logging

from prometheus_client import Counter, Gauge, start_http_server

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MessageQueue(message_pb2_grpc.MessageQueueServicer):
    def __init__(self, broker_manager: BrokerManager):
        self.broker_manager = broker_manager

    def Push(self, request, context):
        queue = self.broker_manager.get_node(request.key)
        if queue.is_alive():
            response = queue.push(request.key, request.value)    
            logger.info(f"Pushed message: {request.key} {request.value}")
        else:
            self.broker_manager.remove_node(queue)
            response = self.Push(request, context)
        return response

    def Pull(self, request, context):
        logger.debug("Pulling message")
        queue = self.broker_manager.get_random_node()
        message = queue.pull()
        logger.info(f"Pulled message: {message.key} {message.value}")
        return message

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
