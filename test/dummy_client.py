### dummy client that passes all tests

from collections import namedtuple
from collections import deque

Message = namedtuple("Message", "key val")
queue: deque = deque()
subscribers: deque = deque()


def push(key: str, val: bytes):
    queue.append(Message(key, val))
    notify_subscribers()

def pull() -> Message:
    return queue.popleft()

def subscribe(action):
    subscribers.append(action)

def notify_subscribers():
    action = subscribers.popleft()
    msg = pull()
    action(msg.key, msg.val)
    subscribers.append(action)
