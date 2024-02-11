# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import zookeeper_pb2 as zookeeper__pb2


class ZookeeperStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ack = channel.unary_unary(
                '/Zookeeper/Ack',
                request_serializer=zookeeper__pb2.Empty.SerializeToString,
                response_deserializer=zookeeper__pb2.Empty.FromString,
                )
        self.Register = channel.unary_unary(
                '/Zookeeper/Register',
                request_serializer=zookeeper__pb2.DiscoveryRequest.SerializeToString,
                response_deserializer=zookeeper__pb2.DiscoveryResponse.FromString,
                )


class ZookeeperServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Ack(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ZookeeperServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Ack': grpc.unary_unary_rpc_method_handler(
                    servicer.Ack,
                    request_deserializer=zookeeper__pb2.Empty.FromString,
                    response_serializer=zookeeper__pb2.Empty.SerializeToString,
            ),
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=zookeeper__pb2.DiscoveryRequest.FromString,
                    response_serializer=zookeeper__pb2.DiscoveryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Zookeeper', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Zookeeper(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Ack(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Zookeeper/Ack',
            zookeeper__pb2.Empty.SerializeToString,
            zookeeper__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Zookeeper/Register',
            zookeeper__pb2.DiscoveryRequest.SerializeToString,
            zookeeper__pb2.DiscoveryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
