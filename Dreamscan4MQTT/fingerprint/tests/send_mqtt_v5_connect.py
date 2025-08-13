import json
import socket
import struct
def send_mqtt_v5_connect(ip, port):
    packet = bytearray()  # bytearray allows for modification
    packet.append(0x10)  # CONNECT

    variable_header = bytearray()
    variable_header += struct.pack("!H", 4)  # sending 4 bytes for 'MQTT'
    variable_header += b'MQTT'  # showing protocol is MQTT
    variable_header.append(5)  # MQTT version 5
    variable_header.append(2)  # Clean Start flag
    variable_header += struct.pack("!H", 60)  # keep alive = 60
    variable_header.append(0x00)  # Properties length = 0
    payload = struct.pack("!H", 0)  # Empty client ID
    remaining_length = len(variable_header) + len(payload)
    packet.append(remaining_length)
    packet += variable_header
    packet += payload
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((ip, port))
            s.send(packet)
            response = s.recv(1024)
        if len(response) >= 4 and response[0] == 0x20:  # CONNACK check
            return_code = response[3]  # Return Code is byte 4
            log = {
                "test": "mqtt_v5_connect",
                "connack_return_code": return_code,

            }
            print(log)
            json_loaded = json.dumps(log)
            with open("results/results.json", "a") as f:
                f.write(json.dumps(log) + "\n")
        else:
            return "[!] Unexpected or malformed response"
    except Exception as e:
        return f"[✗] Connection failed or dropped: {e}"



send_mqtt_v5_connect('192.168.15.211',1883)
