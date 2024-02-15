import pytest
from client.python import kafka_client as python_client

import logging

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup():
    python_client.init_test_mode()
    if python_client.GATEWAY_URL != 'http://localhost:8082':
        LOGGER.error(f"Gateway URL is set to {python_client.GATEWAY_URL}")
        exit(1)


# simple test which gets passed for all clients
def test_answer():
    if python_client.GATEWAY_URL == 'http://localhost:8082':
        assert True


# def test_order():
#     # this test checks if the order garantee holds, i.e. if (k1,v1) is pushed before (k1,v2)
#     # then it is read before (k1,v2)
#
#     TEST_SIZE = 10 * 100
#     KEY_SIZE = 8
#     SUBSCRIER_COUNT = 4
#
#     key_seq = [i % KEY_SIZE for i in range(TEST_SIZE)]
#
#     pulled = {}
#     for i in range(KEY_SIZE):
#         pulled[f"{i}"] = []
#
#     def validate_pull(key, val):
#         next_val = int(val.decode("utf-8"))
#         if len(pulled[key]) != 0:
#             prev_val = pulled[key][-1]
#             if prev_val >= next_val:
#                 print(f"order violation, seq: [{prev_val}, {next_val}]\tkey: [{key}]")
#         pulled[key].append(next_val)
#
#     for _ in range(SUBSCRIER_COUNT):
#         python_client.subscribe(validate_pull)
#
#     for i in range(TEST_SIZE):
#         python_client.push(f"{key_seq[i]}", f"{i}".encode(encoding="utf-8"))
#
#     print("order test passed successfully!")




# def test_push_pull_many():
#     for i in range(100):
#         python_client.push(f"key_{i}", f"value_{i}".encode("utf-8"))
#     num_failed = 0
#     for i in range(100):
#         key, value = python_client.pull()
#         if key != f"key_{i}" or value != f"value_{i}".encode("utf-8"):
#             num_failed += 1
#     assert num_failed == 0



def test_pull_is_blocking():
    '''
    this test checks if the pull method is blocking
    i.e. if there is no message in the queue, the pull method should wait until a message is pushed
    one thread pulls, the other waits for 10 seconds and then pushes a message
    the pull thread should then return the pushed message after 10 seconds
    '''
    import threading
    import time

    def push_after_10_seconds():
        time.sleep(10)
        python_client.push("test_pull_is_blocking", "test_pull_is_blocking".encode("utf-8"))

    t = threading.Thread(target=push_after_10_seconds)
    t.start()
    key, value = python_client.pull()
    assert key == "test_pull_is_blocking"
    assert value == "test_pull_is_blocking".encode("utf-8")



