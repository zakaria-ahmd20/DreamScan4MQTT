import paho.mqtt.client as mqtt
import json
import time
import signal
import sys
import os
# Timeout handler for safety
def handler(signum, frame):
    print("[!] Timeout reached, exiting...")
    sys.exit(1)

#signal.signal(signal.SIGALRM, handler)
#signal.alarm(5)  # 5 seconds timeout
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'config', 'config.json'))
results_file = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'results', 'auth-check.json'))
# Step 3: Load JSON config
with open(config_path, 'r') as f:
    config = json.load(f)

broker_ip = str(config['broker_ip'])
broker_port = int(config['broker_port'])


connected = False

def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        connected = True
        print("[+] Connected without authentication!")
    else:
        print(f"[!] Connection rejected with code {rc}")

def on_disconnect(client, userdata, rc):
    print("[*] Disconnected")

client = mqtt.Client(client_id="unauth_check_test", clean_session=True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

print(f"[*] Trying to connect to {broker_ip}:{broker_port} without username/password...")

result = {}
try:
    client.connect(broker_ip, broker_port, 60)
except Exception as e:
    print(f"[!] Connection error: {e}")
    result = {
        "test": "Unauthorized access check",
        "result": f"Connection error: {e}"
    }
else:
    client.loop_start()
    time.sleep(3)  # wait a few seconds for connection callback
    client.loop_stop()
    client.disconnect()

    if connected:
        result = {
            "test": "Unauthorized access check",
            "result": "Broker allows unauthenticated connection."
        }
    else:
        result = {
            "test": "Unauthorized access check",
            "result": "Broker rejects unauthenticated connection."
        }

# Save result to file
try:
    with open(results_file, "a") as f:
        f.write(json.dumps(result) + "\n")
except Exception as e:
    print(f"[!] Error writing to results file: {e}")

print(json.dumps(result, indent=2))
