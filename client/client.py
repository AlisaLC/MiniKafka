import requests
import os
import base64
import json
import threading

def blocking_request(method: str, url: str, data: bytes, headers: dict) -> bytes:
    response = None
    while response is None:
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, data=data, headers=headers)
        except requests.exceptions.ConnectionError:
            pass
    return response

def push(key: str, value) -> None:
    url = os.getenv("API_GATEWAY_URL") + "/push"
    value = base64.b64encode(value).decode("utf-8")
    data = {"key": key, "value": value}
    blocking_request("POST", url, data, {})

def pull() -> bytes:
    url = os.getenv("API_GATEWAY_URL") + "/pull"
    response = blocking_request("GET", url, None, {})
    data = json.loads(response.content)
    key = data["key"]
    value = base64.b64decode(data["value"])
    return key, value

def subscribe_thread(f: callable[[str, bytes], None]) -> None:
    while True:
        key, value = pull()
        f(key, value)

def subscribe(f: callable[[str, bytes], None]) -> None:
    thread = threading.Thread(target=subscribe_thread, args=(f,))
    thread.start()