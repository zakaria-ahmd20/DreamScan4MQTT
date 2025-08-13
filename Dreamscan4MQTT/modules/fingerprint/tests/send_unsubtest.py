import json
import socket
import struct
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
results_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'results', 'results.json'))
config_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'config', 'config.json'))
with open(config_path, 'r') as f:
    config = json.load(f)
ip = str(config['broker_ip'])
port = int(config['broker_port'])
def encode_remaining_length(length):
    encoded = b''
    while True:
        byte = length % 128
        length //= 128
        if length > 0:
            byte |= 0x80
        encoded += struct.pack("B", byte)
        if length == 0:
            break
    return encoded

def build_zero_length_unsub():
    packet_id = b'\x00\x0A'  # Packet Identifier (required > 0)
    zero_topic = b'\x00\x00'  # Zero-length topic filter
    payload = zero_topic
    variable_header = packet_id
    remaining_length = len(variable_header) + len(payload)
    fixed_header = b'\xA2' + encode_remaining_length(remaining_length)  # UNSUBSCRIBE
    return fixed_header + variable_header + payload

def send_unsub_test(ip, port):
    connect = (
        b'\x10' b'\x12' b'\x00\x06MQIsdp'
        b'\x03' b'\x02' b'\x00\x3c' b'\x00\x04test'
    )
    try:
        sock = socket.create_connection((ip, port), timeout=5)
        sock.sendall(connect)
        connack = sock.recv(4)
        if len(connack) < 4:
            return {"test": "unsub_test", "error": "Incomplete CONNACK"}
    except Exception:
        return {"test": "unsub_test", "error": "Connection or CONNACK error"}

    try:
        unsub = build_zero_length_unsub()
        sock.sendall(unsub)
        resp = sock.recv(1024)
        if resp:
            result = f"Response received: {resp.hex()}"
        else:
            result = "Connection closed by broker with no response."
    except ConnectionResetError:
        result = "Connection reset by peer (forceful disconnect)."
    finally:
        sock.close()

    log = {
        "test": "unsub_test",
        "result": result
    }
    print(log)
    with open(results_path, "a") as f:

        json_line = json.dumps(log) + "\n"
        print(f"Appending: {json_line.strip()}")
        f.write(json_line)
    return log


send_unsub_test(ip,port)
