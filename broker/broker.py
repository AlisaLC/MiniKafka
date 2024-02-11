from proto.zookeeper_pb2 import DiscoveryRequest, Status, Empty as ZookeeperEmpty
import proto.zookeeper_pb2_grpc
from proto.broker_pb2 import Empty as BrokerEmpty, PushResponse, Status, Message, MessageList, MessageCount, PullResponse
import proto.broker_pb2_grpc as broker_pb2_grpc
import grpc

from concurrent.futures import ThreadPoolExecutor
import os
import time

class BrokerServer(broker_pb2_grpc.BrokerServicer):
    def __init__(self) -> None:
        self.uuid = os.urandom(16).hex()
        self.messages = []
        self.replica_messages = []
        self.replica = None
        self.replica_stub = None

    def Ack(self, request, context):
        return BrokerEmpty()
    
    def Push(self, request, context):
        self.messages.append((request.key, request.value))
        if self.replica:
            self.replica_stub.PushReplica(MessageList(messages=[Message(key=request.key, value=request.value)]))
        return PushResponse(status=Status.SUCCESS, message="")
    
    def Pull(self, request, context):
        if not self.messages:
            for i in range(10):
                time.sleep(1)
                if self.messages:
                    break
            else:
                return PullResponse(status=Status.FAILURE, message="No messages")
        key, value = self.messages.pop(0)
        if self.replica:
            self.replica_stub.DropReplicaMessages(MessageCount(count=1))
        return PullResponse(status=Status.SUCCESS, message=Message(key=key, value=value))
    
    def SetReplica(self, request, context):
        self.replica = request.uuid
        self.replica_stub = proto.broker_pb2_grpc.BrokerStub(grpc.insecure_channel(request.url))
        batch = 10
        for i in range(0, len(self.messages), batch):
            self.replica_stub.PushReplica(MessageList(messages=[Message(key=k, value=v) for k, v in self.messages[i:i+batch]]))
        return BrokerEmpty()
    
    def LeadReplica(self, request, context):
        if not self.replica:
            raise Exception("No replica")
        self.messages.extend(self.replica_messages)
        self.replica_messages.clear()
        return BrokerEmpty()
    
    def DropReplica(self, request, context):
        self.replica = None
        self.replica_messages.clear()
        return BrokerEmpty()
    
    def PushReplica(self, request, context):
        for message in request.messages:
            self.replica_messages.append((message.key, message.value))
        return BrokerEmpty()
    
    def DropReplicaMessages(self, request, context):
        self.replica_messages = self.replica_messages[request.count:]
        return BrokerEmpty()
    
if __name__ == "__main__":
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    broker = BrokerServer()
    broker_pb2_grpc.add_BrokerServicer_to_server(broker, server)
    server.add_insecure_port(f'[::]:{os.environ["BROKER_PORT"]}')
    server.start()
    channel = grpc.insecure_channel(f'{os.environ["ZOOKEEPER_HOST"]}:{os.environ["ZOOKEEPER_PORT"]}')
    stub = proto.zookeeper_pb2_grpc.ZookeeperStub(channel)
    stub.Register(DiscoveryRequest(url=f'{os.environ["BROKER_HOST"]}:{os.environ["BROKER_PORT"]}', uuid=broker.uuid))
    server.wait_for_termination()