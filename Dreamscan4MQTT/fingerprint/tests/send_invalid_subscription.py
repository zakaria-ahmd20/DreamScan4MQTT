import json
import socket
import struct

def encode_length(length):
    encoded = b""
    while True:
        digit = length % 128
        length //= 128
        if length > 0:
            digit |= 0x80
        encoded += struct.pack("!B", digit)
        if length == 0:
            break
    return encoded


def send_invalid_subscribe(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ip, port))

        proto_name = b"MQIsdp"
        vh = (
            struct.pack("!H", len(proto_name)) + proto_name +
            struct.pack("!B", 3) +  # Protocol level
            struct.pack("!B", 0x02) +  # Clean session
            struct.pack("!H", 60)
        )
        pl = struct.pack("!H", 9) + b"rawclient"
        connect = struct.pack("!B", 0x10) + encode_length(len(vh) + len(pl)) + vh + pl

        s.sendall(connect)
        connack = s.recv(4)
        print(connack.hex())

        topic = b"foo/+bar"
        tf = struct.pack("!H", len(topic)) + topic + b'\x00'
        vh = struct.pack("!H", 1)
        subscribe = struct.pack("!B", 0x82) + encode_length(len(vh) + len(tf)) + vh + tf

        s.sendall(subscribe)
        suback = s.recv(5)
        result = suback.hex()
        print(result)
        if len(result) > 0:
            log = {
                "test": "Reject invalid un/subscriptions  ",
                "result": 'Not Rejected '
            }
            json_loaded = json.dumps(log)
            with open("results/results.json", "a") as f:
                f.write(json.dumps(log) + "\n")
        else:
            log = {
                "test": "Reject invalid un/subscriptions  ",
                "result": 'Rejected '
            }
            json_loaded = json.dumps(log)
            with open("results/results.json", "a") as f:
                f.write(json.dumps(log) + "\n")

        s.close()
    except Exception as e:
        result = f"[!] SUBSCRIBE error: {e}"
    print(result)


ip = "192.168.15.211"
port = 1883
send_invalid_subscribe(ip, port)
