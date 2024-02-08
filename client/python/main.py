import kafka_client as client

if __name__ == '__main__':
    while True:
        cmd = input("CMD: ").strip().upper()
        if cmd == "PUSH":
            key = input("KEY: ")
            value = input("VALUE: ")
            client.push(key, value.encode("utf-8"))
        elif cmd == "PULL":
            key, value = client.pull()
            print(f"key: {key}, value: {value.decode('utf-8')}")
        else:
            print("unknown command")
