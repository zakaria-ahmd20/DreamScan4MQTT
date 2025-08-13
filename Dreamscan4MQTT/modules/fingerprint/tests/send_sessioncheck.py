import json
import socket
import struct
import time
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
results_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'results', 'results.json'))
config_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'config', 'config.json'))
with open(config_path, 'r') as f:
    config = json.load(f)
ip = str(config['broker_ip'])
port = int(config['broker_port'])
def connect_and_check_session(ip, port, client_id, clean_session):
    # MQTT Fixed Header
    packet = bytearray()
    packet.append(0x10)  # CONNECT packet type

    # Variable Header
    vh = bytearray()
    vh += struct.pack("!H", 4) + b'MQTT'  # Protocol Name
    vh.append(4)  # Protocol level (4 = MQTT 3.1.1)
    flags = 0x02 if clean_session else 0x00
    vh.append(flags)  # Clean session flag
    vh += struct.pack("!H", 60)  # Keep Alive: 60 seconds

    # Payload
    payload = struct.pack("!H", len(client_id)) + client_id.encode()

    remaining_length = len(vh) + len(payload)
    packet.append(remaining_length)
    packet += vh + payload

    try:
        with socket.create_connection((ip, port), timeout=3) as s:
            s.sendall(packet)
            resp = s.recv(4)
            if len(resp) == 4 and resp[0] == 0x20:
                session_present = resp[2] & 0x01
                return session_present, resp
            else:
                return None, resp
    except Exception as e:
        print(f"[!] Error: {e}")
        return None, None

ip = "192.168.15.211"
port = 1883
client_id = "sessiontest"

print("[*] Connecting first time...")
sp1, r1 = connect_and_check_session(ip, port, client_id, clean_session=False)
print(f"→ 1st CONNACK: {r1.hex() if r1 else 'None'} | Session Present: {sp1}")

time.sleep(1)  # short pause between connects

print("[*] Connecting second time...")
sp2, r2 = connect_and_check_session(ip, port, client_id, clean_session=False)
print(f"→ 2nd CONNACK: {r2.hex() if r2 else 'None'} | Session Present: {sp2}")

if sp2 == 1:
    print("session present supported")
    log = {
        "test": "session present check",
        "result": 'session present supported'
    }

    print(log)
    json_loaded = json.dumps(log)
    with open(results_path, "a") as f:

        f.write(json.dumps(log) + "\n")


elif sp2 == 0:
    print("session present not supported")
    log = {
        "test": "session present check",
        "result": 'session present not supported'
    }

    print(log)
    json_loaded = json.dumps(log)
    with open(results_path, "a") as f:

        f.write(json.dumps(log) + "\n")
else:
    print("\n[!] Unexpected response or error.")
