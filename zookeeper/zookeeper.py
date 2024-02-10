import grpc
from proto.message_pb2 import Message, PushResponse, PushStatus
import proto.message_pb2_grpc as message_pb2_grpc
import os
import time
from concurrent.futures import ThreadPoolExecutor
import logging
from hashring import ConsistentHashRing
from prometheus_client import Counter, Gauge, start_http_server

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

hash_ring = ConsistentHashRing()

PUSH_COUNTER = Counter("zookeeper_push_counter", "Number of messages pushed", ["queue", "key"])
PULL_COUNTER = Counter("zookeeper_pull_counter", "Number of messages pulled", ["queue", "key"])
BROKER_COUNTER = Gauge("zookeeper_broker_counter", "Number of brokers", ["name"])
BROKER_MESSAGE_COUNTER = Gauge("zookeeper_broker_message_counter", "Number of messages in broker", ["queue"])


class MessageQueue(message_pb2_grpc.MessageQueueServicer):
    def __init__(self):
        self.broker_count = int(os.environ.get("BROKERS", 5))
        self.queues = []
        for i in range(self.broker_count):
            self.queues.append([])
            hash_ring.add_node(f"broker-{i}")
            BROKER_COUNTER.labels(name=f"broker-{i}").inc()
        self.mapping = {f"broker-{i}": i for i in range(self.broker_count)}

    def Push(self, request, context):
        queue_id = self.mapping[hash_ring.get_node(request.key)]
        logger.debug(f"Pushing message to queue {queue_id}")
        queue = self.queues[queue_id]
        queue.append((request.key, request.value))
        PUSH_COUNTER.labels(queue=f"{queue_id}", key=request.key).inc()
        BROKER_MESSAGE_COUNTER.labels(queue=f"{queue_id}").inc()
        logger.info(f"Pushed message: {request.key} {request.value}")
        return PushResponse(status=PushStatus.SUCCESS, message="")

    def Pull(self, request, context):
        logger.debug("Pulling message")
        while True:
            for i, queue in enumerate(self.queues):
                if queue:
                    message = queue.pop(0)
                    PULL_COUNTER.labels(queue=f"{i}", key=message[0]).inc()
                    BROKER_MESSAGE_COUNTER.labels(queue=f"{i}").dec()
                    logger.debug(f"Pulled from queue {i}")
                    break
            else:
                time.sleep(1)
                continue
            break
        logger.info(f"Pulled message: {message[0]} {message[1]}")
        return Message(key=message[0], value=message[1])
    
if __name__ == "__main__":
    start_http_server(8000)
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessageQueueServicer_to_server(MessageQueue(), server)
    server.add_insecure_port(f"[::]:{os.getenv('ZOOKEEPER_PORT')}")
    server.start()
    server.wait_for_termination()
