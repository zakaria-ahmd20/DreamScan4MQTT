import os
import paho.mqtt.client as paho
import re
import requests
import json


def versionscan():
    done = False  # flag to wait until data is written

    # Calculate absolute path to results folder at project root:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))  # go up from scripts/
    results_dir = os.path.join(project_root, 'results')
    json_path = os.path.join(results_dir, "mqtt_cve_data.json")
    config_path = os.path.abspath(os.path.join(base_dir, '..', 'config', 'config.json'))
    with open(config_path, 'r') as f:
        config = json.load(f)
    broker_ip = str(config['broker_ip'])
    broker_port = int(config['broker_port'])

    def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed:", mid, granted_qos)

    def on_message(client, userdata, msg):
        nonlocal done
        version_string_raw = msg.payload.decode('utf-8')
        print("Raw Broker Version:", version_string_raw)
        match = re.search(r"version (\d+\.\d+(\.\d+)*)", version_string_raw)
        if match:
            extracted_version = match.group(1)
            cpe_23_string = f"cpe:2.3:a:eclipse:mosquitto:{extracted_version}:*:*:*:*:*:*:*"
            print("Detected Version:", extracted_version)
            print("CPE:", cpe_23_string)

            try:
                response = requests.get(f'https://cvedb.shodan.io/cves?cpe23={cpe_23_string}', timeout=10)
                response.raise_for_status()
                cve_data = response.json()

                report = {
                    "broker_ip": broker_ip,
                    "broker_port": broker_port,
                    "version_raw": version_string_raw,
                    "version": extracted_version,
                    "cpe": cpe_23_string,
                    "cves": {"cves": cve_data}
                }

                with open(json_path, "w") as f:
                    json.dump(report, f, indent=2)

                print(f"JSON saved to {json_path}")
                done = True
                client.disconnect()

            except requests.exceptions.RequestException as e:
                print("Error fetching CVE data:", e)
                done = True
                client.disconnect()

            except json.JSONDecodeError:
                print("Error decoding CVE JSON.")
                done = True
                client.disconnect()
        else:
            print("Could not extract version.")
            print("Payload received:", version_string_raw)
            done = True
            client.disconnect()

    client = paho.Client()
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    try:
        client.connect(broker_ip, broker_port)
    except Exception as e:
        print("Could not connect to broker:", e)
        return

    client.subscribe('$SYS/broker/version', qos=1)
    client.loop_start()

    while not done:
        pass

    client.loop_stop()
