import grpc
import os
import time
import logging
from prometheus_client import start_http_server, Counter, Gauge
from concurrent.futures import ThreadPoolExecutor

from proto.zookeeper_pb2 import DiscoveryRequest
import proto.zookeeper_pb2_grpc
from proto.broker_pb2 import BrokerEmpty, BrokerPushResponse, BrokerStatus, BrokerMessage, MessageList, MessageCount,\
    BrokerPullResponse
import proto.broker_pb2_grpc as broker_pb2_grpc

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PUSH_COUNTER = Counter("broker_push_counter", "Number of push to broker")
PULL_COUNTER = Counter("broker_pull_counter", "Number of pull from broker")
MESSAGES_LENGTH = Gauge("broker_message_len", "Number of messages in broker")
REPLICA_MESSAGES_LENGTH = Gauge("broker_replica_messages_len", "Number of replica messages in broker")


class BrokerServer(broker_pb2_grpc.BrokerServicer):
    def __init__(self) -> None:
        self.uuid = os.urandom(16).hex()
        self.messages = []
        self.replica_messages = []
        self.replica = None
        self.replica_stub = None

    def __is_replica_alive(self):
        if not self.replica:
            return False
        try:
            self.replica_stub.Ack(BrokerEmpty())
        except:
            logger.error(f"Replica {self.replica} is not alive")
            self.replica = None
            self.replica_stub = None
            if self.replica_messages:
                logger.warning(f"Replica {self.replica} has {len(self.replica_messages)} messages")
                self.messages.extend(self.replica_messages)
                MESSAGES_LENGTH.inc(len(self.replica_messages))
                self.replica_messages.clear()
                REPLICA_MESSAGES_LENGTH.set(0)
            return False
        logger.debug(f"Replica {self.replica} is alive")
        return True

    def Ack(self, request, context):
        return BrokerEmpty()
    
    def Push(self, request, context):
        self.messages.append((request.key, request.value))
        logger.info(f"Pushed message {request.key} {request.value}")
        PUSH_COUNTER.inc()
        MESSAGES_LENGTH.inc()
        if self.__is_replica_alive():
            self.replica_stub.PushReplica(MessageList(messages=[BrokerMessage(key=request.key, value=request.value)]))
        return BrokerPushResponse(status=BrokerStatus.BROKER_SUCCESS, message="")
    
    def Pull(self, request, context):
        if not self.messages:
            logger.error(f"Pulling message {self.uuid} failed!\nBroker is not available")
            return BrokerPullResponse(status=BrokerStatus.BROKER_FAILURE, message="No messages")
        key, value = self.messages.pop(0)
        logger.warning(f"Pulled message from Broker {self.uuid}: {key} {value}")
        PULL_COUNTER.inc()
        MESSAGES_LENGTH.dec()
        if self.__is_replica_alive():
            self.replica_stub.DropReplicaMessages(MessageCount(count=1))
        return BrokerPullResponse(status=BrokerStatus.BROKER_SUCCESS, message=BrokerMessage(key=key, value=value))
    
    def SetReplica(self, request, context):
        self.replica = request.uuid
        self.replica_stub = proto.broker_pb2_grpc.BrokerStub(grpc.insecure_channel(request.url))
        if not self.__is_replica_alive():
            logger.error(f"Replica {request.uuid} is not available")
            return BrokerEmpty()
        logger.info(f"Set replica for broker {self.uuid}: {request.uuid}")
        batch = 10
        for i in range(0, len(self.messages), batch):
            self.replica_stub.PushReplica(MessageList(
                messages=[BrokerMessage(key=k, value=v) for k, v in self.messages[i:i+batch]]
            ))
        return BrokerEmpty()
    
    def LeadReplica(self, request, context):
        if len(self.replica_messages) == 0:
            return BrokerEmpty()
        logger.info(f"Merging replica messages to queue messages of broker {self.uuid}")
        self.messages.extend(self.replica_messages)
        MESSAGES_LENGTH.inc(len(self.replica_messages))
        if self.__is_replica_alive():
            batch = 10
            for i in range(0, len(self.messages), batch):
                self.replica_stub.PushReplica(MessageList(
                    messages=[BrokerMessage(key=k, value=v) for k, v in self.messages[i:i+batch]]
                ))
        self.replica_messages.clear()
        REPLICA_MESSAGES_LENGTH.set(0)
        return BrokerEmpty()
    
    def DropReplica(self, request, context):
        logger.warning(f"Dropping broker {self.uuid} replica")
        self.replica_messages.clear()
        REPLICA_MESSAGES_LENGTH.set(0)
        return BrokerEmpty()
    
    def PushReplica(self, request, context):
        for message in request.messages:
            self.replica_messages.append((message.key, message.value))
            REPLICA_MESSAGES_LENGTH.inc()
            logger.info(f"Pushed message {message.key} {message.value} to replica messages")
        return BrokerEmpty()
    
    def DropReplicaMessages(self, request, context):
        logger.warning(f"Dropping {request.count} message from replica messages")
        self.replica_messages = self.replica_messages[request.count:]
        REPLICA_MESSAGES_LENGTH.dec(request.count)
        return BrokerEmpty()


if __name__ == "__main__":
    start_http_server(8000)
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    broker = BrokerServer()
    broker_pb2_grpc.add_BrokerServicer_to_server(broker, server)
    server.add_insecure_port(f'0.0.0.0:{os.environ["BROKER_PORT"]}')
    server.start()
    channel = grpc.insecure_channel(f'{os.environ["ZOOKEEPER_HOST"]}:{os.environ["ZOOKEEPER_PORT"]}')
    stub = proto.zookeeper_pb2_grpc.ZookeeperStub(channel)
    stub.Register(DiscoveryRequest(url=f'{os.environ["BROKER_HOST"]}:{os.environ["BROKER_PORT"]}', uuid=broker.uuid))
    server.wait_for_termination()
