import json

# Load lines from file, each line is a JSON object
with open('results/results.json') as f:
    lines = [json.loads(line) for line in f]

# Define expected tests and expected key-value pairs for each
expected = [
    {"test": "Reject invalid un/subscriptions  ", "result": "Rejected "},
    {"test": "mqtt_v5_connect", "connack_return_code": 1},
    {"test": "session present check", "result": "session present not supported"},
    {"test": "unsub_test", "result": "Connection closed by broker with no response."}
]

def matches(expected_entry, actual_entry):
    # Check if all keys in expected_entry match in actual_entry exactly (including spaces)
    for k, v in expected_entry.items():
        if actual_entry.get(k) != v:
            return False
    return True

# Check if each expected entry has a matching line in the JSON file
all_found = True
for exp in expected:
    if not any(matches(exp, line) for line in lines):
        all_found = False
        break

if all_found:
    print("This looks like Mosquitto™ 1.3.1-1.3.5")
    log = {
        "test": "Fingerprint  ",
        "result": 'Mosquitto™ 1.3.1-1.3.5"'
    }
    json_loaded = json.dumps(log)
    with open("rules-matched.json", "a") as f:
        f.write(json.dumps(log) + "\n")
else:
    print("Does NOT match Mosquitto™ 1.3.1-1.3.5")
