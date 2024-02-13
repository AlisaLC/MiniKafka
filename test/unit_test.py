import unittest


from client.python import kafka_client as python_client
from client.go import client as go_client


# simple test which gets passed for all clients
def test_true():
    assert True
