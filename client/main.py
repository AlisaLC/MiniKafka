import client

if __name__ == '__main__':
    while True:
        cmd = input().strip().lower()
        if cmd == "push":
            key = input("key: ")
            value = input("value: ")
            client.push(key, value.encode("utf-8"))
        elif cmd == "pull":
            key, value = client.pull()
            print(f"key: {key}, value: {value.decode('utf-8')}")
        else:
            print("unknown command")