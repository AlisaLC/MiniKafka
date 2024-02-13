from proto.broker_pb2 import BrokerEmpty, BrokerMessage, ReplicaRequest, BrokerStatus
import proto.broker_pb2_grpc
import grpc

import random
import bisect
import threading

from hashring import ConsistentHashRing

from prometheus_client import Gauge, Counter
BROKER_COUNTER = Gauge("zookeeper_broker_counter", "Number of brokers", ["name"])
PUSH_COUNTER = Counter("zookeeper_push_counter", "Number of messages pushed", ["queue", "key"])
PULL_COUNTER = Counter("zookeeper_pull_counter", "Number of messages pulled", ["queue", "key"])
BROKER_MESSAGE_COUNTER = Gauge("zookeeper_broker_message_counter", "Number of messages in broker", ["queue"])

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Broker:
    def __init__(self, uuid, url) -> None:
        self.uuid = uuid
        self.url = url
        self.stub = None
        self.replica = None

    def connect(self):
        if self.stub:
            return
        self.stub = proto.broker_pb2_grpc.BrokerStub(grpc.insecure_channel(self.url))

    def is_alive(self):
        try:
            self.stub.Ack(BrokerEmpty())
        except:
            logger.error(f"Broker {self.uuid} is not alive")
            return False
        logger.debug(f"Broker {self.uuid} is alive")
        return True
    
    def push(self, key, value):
        response = self.stub.Push(BrokerMessage(key=key, value=value))
        if response.status == BrokerStatus.BROKER_SUCCESS:
            PUSH_COUNTER.labels(queue=self.uuid, key=key).inc()
            BROKER_MESSAGE_COUNTER.labels(queue=self.uuid).inc()
        return response
    
    def pull(self):
        response = self.stub.Pull(BrokerEmpty())
        if response.status == BrokerStatus.BROKER_SUCCESS:
            PULL_COUNTER.labels(queue=self.uuid, key=response.message.key).inc()
            BROKER_MESSAGE_COUNTER.labels(queue=self.uuid).dec()
        return response
    
    def set_replica(self, replica):
        logger.info(f"Setting replica for {self.uuid} to {replica.uuid}")
        self.replica = replica
        response = self.stub.SetReplica(ReplicaRequest(uuid=replica.uuid, url=replica.url))
        return response
    
    def lead_replica(self):
        logger.info(f"Leading replica for {self.uuid}")
        return self.stub.LeadReplica(BrokerEmpty())
    
    def drop_replica(self):
        logger.info(f"Dropping replica for {self.uuid}")
        return self.stub.DropReplica(BrokerEmpty())

    def __str__(self) -> str:
        return self.uuid

class BrokerManager:
    def __init__(self) -> None:
        self.hash_ring = ConsistentHashRing()
        self.brokers = {}
        self.broker_ring = []
        self.lock = threading.Lock()

    def add_node(self, node: str):
        if node.uuid in self.brokers:
            logger.debug(f"Broker {node.uuid} already exists")
            return
        node.connect()
        if not node.is_alive():
            return
        with self.lock:
            self.hash_ring.add_node(node)
            self.brokers[node.uuid] = node
            BROKER_COUNTER.labels(name=node.uuid).inc()
            self.__add_node_to_chain(node)
        logger.info(f"Added broker {node.uuid}")

    def __add_node_to_chain(self, node):
        bisect.insort(self.broker_ring, node.uuid)
        if len(self.broker_ring) < 2:
            return
        index = self.broker_ring.index(node.uuid)
        replica_index = (index + 1) % len(self.broker_ring)
        prev_replica_index = (index - 1) % len(self.broker_ring)
        replica = self.brokers[self.broker_ring[replica_index]]
        prev_replica = self.brokers[self.broker_ring[prev_replica_index]]
        replica.drop_replica()
        node.set_replica(replica)
        prev_replica.set_replica(node)

    def remove_node(self, node: str):
        if node.uuid not in self.brokers or len(self.broker_ring) == 0:
            logger.debug(f"Broker {node.uuid} does not exist")
            return
        with self.lock:
            if len(self.broker_ring) > 2:
                self.__remove_node_from_chain(node)
            self.hash_ring.remove_node(node)
            del self.brokers[node.uuid]
            self.broker_ring.remove(node.uuid)
            if len(self.broker_ring) == 1:
                self.brokers[self.broker_ring[0]].lead_replica()
            BROKER_COUNTER.labels(name=node.uuid).dec()
        logger.info(f"Removed broker {node.uuid}")

    def __remove_node_from_chain(self, node):
        index = self.broker_ring.index(node.uuid)
        replica_index = (index + 1) % len(self.broker_ring)
        prev_replica_index = (index - 1) % len(self.broker_ring)
        replica = self.brokers[self.broker_ring[replica_index]]
        prev_replica = self.brokers[self.broker_ring[prev_replica_index]]
        node_message_count = BROKER_MESSAGE_COUNTER.labels(queue=node.uuid)._value.get()
        replica_message_count = BROKER_MESSAGE_COUNTER.labels(queue=replica.uuid)._value.get()
        BROKER_MESSAGE_COUNTER.labels(queue=replica.uuid).set(replica_message_count + node_message_count)
        BROKER_MESSAGE_COUNTER.remove(queue=node.uuid)
        replica.lead_replica()
        prev_replica.set_replica(replica)

    def get_node(self, key: str):
        if len(self.brokers) == 0:
            return None
        node = self.hash_ring.get_node(key)
        if node.is_alive():
            return node
        self.remove_node(node)
        return self.get_node(key)
    
    def get_random_node(self):
        if len(self.brokers) == 0:
            return None
        node = random.choice(list(self.brokers.values()))
        if node.is_alive():
            return node
        self.remove_node(node)
        return self.get_random_node()