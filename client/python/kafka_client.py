from typing import Callable

import requests
import json

import os
import base64
import time
import threading

import dotenv
dotenv.load_dotenv()

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

GATEWAY_URL = f'http://{os.getenv("GATEWAY_HOST")}:{os.getenv("GATEWAY_PORT")}'

logger.info(f"Gateway URL: {GATEWAY_URL}")

def blocking_request(method: str, url: str, data: bytes, headers: dict) -> bytes:
    response = None
    while response is None:
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, data=data, headers=headers)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"{e} occurred")
        if response.status_code != 200:
            response = None
            time.sleep(1)
    return response

def push(key: str, value) -> None:
    url = GATEWAY_URL + "/push"
    value = base64.b64encode(value).decode("utf-8")
    logger.info(f"Pushing message: {key} {value}")
    data = {"key": key, "value": value}
    response = blocking_request("POST", url, data, {})
    logger.info(f"Push response: {response.content}")

def pull() -> bytes:
    url = GATEWAY_URL + "/pull"
    response = blocking_request("GET", url, None, {})
    logger.info(f"Pulled message: {response.content}")
    logger.info(f"Status code: {response.status_code}")
    data = json.loads(response.content)
    key = data["key"]
    value = base64.b64decode(data["value"])
    return key, value

def subscribe_thread(f: Callable[[str, bytes], None]) -> None:
    while True:
        key, value = pull()
        f(key, value)

def subscribe(f: Callable[[str, bytes], None]) -> None:
    thread = threading.Thread(target=subscribe_thread, args=(f,))
    thread.start()
