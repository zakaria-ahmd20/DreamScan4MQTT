import os
import json
import rule_engine

# Define rules
rules = [
    rule_engine.Rule('test == "Unauthorized access check" and result == "Broker allows unauthenticated connection."'),
    rule_engine.Rule('test == "Unauthorized access check" and result == "Broker rejects unauthenticated connection."'),
]

rules_matched = []

# Compute absolute path to results.json (adjust as needed)
base_dir = os.path.dirname(os.path.abspath(__file__))
results_path = os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'results', 'auth-check.json'))

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

if len(rules_matched) == 1:
    print("Auth check complete - found unauthenticated access allowed.")
elif len(rules_matched) == 0:
    print("Auth is enforced")
