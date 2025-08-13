import paho.mqtt.client as paho
import re
import requests
import json

def versionscan():
    broker_ip = input('Broker IP: ')
    broker_port = int(input('Broker Port: '))

    done = False  # flag to wait until data is written

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

                with open("results/mqtt_cve_data.json", "w") as f:
                    json.dump(report, f, indent=2)

                print("JSON saved to mqtt_cve_data.json")
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
