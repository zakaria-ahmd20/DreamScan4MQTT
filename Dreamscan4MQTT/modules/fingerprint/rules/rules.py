import os
import json
import rule_engine

# Define base_dir and paths upfront
base_dir = os.path.dirname(os.path.abspath(__file__))

results_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'results', 'results.json'))
output_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'results', 'fingerprint-matched.json'))

# Define rules
rules = [
    rule_engine.Rule('test == "mqtt_v5_connect" and connack_return_code == 1'),
    rule_engine.Rule('test == "unsub_test" and result == "Connection closed by broker with no response."'),
    rule_engine.Rule('test == "Reject invalid un/subscriptions" and result == "Rejected"'),
    rule_engine.Rule('test == "session present check" and result == "session present not supported"')
]

rules_matched = []

# Read and check each line
with open(results_path, "r") as f:
    for line in f:
        data = json.loads(line)
        matched = False
        for rule in rules:
            if rule.matches(data):
                print("Rule matched:", data)
                matched = True
                rules_matched.append(1)
        if not matched:
            print("No match:", data)

if len(rules_matched) == 4:
    print("Mosquitto™ 1.3.1-1.3.5")
    log = {
        "fingerprint": "Mosquitto™ 1.3.1-1.3.5"
    }

    with open(output_path, "w") as f:
        json.dump(log, f, indent=2)
