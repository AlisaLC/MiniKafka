import unittest

from client.python import kafka_client as python_client
from client.go import client as go_client


# simple test which gets passed for all clients
class TestClient(unittest.TestCase):
    def always_pass(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
