# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import message_pb2 as message__pb2


class MessageQueueStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Push = channel.unary_unary(
                '/MessageQueue/Push',
                request_serializer=message__pb2.Message.SerializeToString,
                response_deserializer=message__pb2.PushResponse.FromString,
                )
        self.Pull = channel.unary_unary(
                '/MessageQueue/Pull',
                request_serializer=message__pb2.Empty.SerializeToString,
                response_deserializer=message__pb2.Message.FromString,
                )


class MessageQueueServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Push(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Pull(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MessageQueueServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Push': grpc.unary_unary_rpc_method_handler(
                    servicer.Push,
                    request_deserializer=message__pb2.Message.FromString,
                    response_serializer=message__pb2.PushResponse.SerializeToString,
            ),
            'Pull': grpc.unary_unary_rpc_method_handler(
                    servicer.Pull,
                    request_deserializer=message__pb2.Empty.FromString,
                    response_serializer=message__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'MessageQueue', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MessageQueue(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Push(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MessageQueue/Push',
            message__pb2.Message.SerializeToString,
            message__pb2.PushResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Pull(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MessageQueue/Pull',
            message__pb2.Empty.SerializeToString,
            message__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)