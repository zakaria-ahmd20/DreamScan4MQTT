import os
import subprocess
import sys
from scripts.version_detection import versionscan
from scripts.generate_report import reportgen



def run_python_script(script_path):
    print(f"\n[+] Running {script_path}")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"[!] Error output:\n{result.stderr}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # project root
    modules_dir = os.path.join(base_dir, 'modules')

    # Step 1: find all module folders (e.g., fingerprint,)
    module_folders = [f.path for f in os.scandir(modules_dir) if f.is_dir()]
    if not module_folders:
        print("[-] No module folders found in modules/")
        return

    for module_folder in module_folders:
        print(f"\n=== [ Module: {os.path.basename(module_folder)} ] ===")

        # Step 2: Run tests/*.py
        tests_dir = os.path.join(module_folder, 'tests')
        if os.path.isdir(tests_dir):
            test_scripts = sorted(f.path for f in os.scandir(tests_dir) if f.is_file() and f.name.endswith('.py'))
            if not test_scripts:
                print("[-] No test scripts found in tests/")
            else:
                for script in test_scripts:
                    run_python_script(script)
        else:
            print(f"[-] tests/ folder not found in {module_folder}")

        # Step 3: Run rules/rules.py
        rules_dir = os.path.join(module_folder, 'rules')
        rules_py = os.path.join(rules_dir, 'rules.py')
        if os.path.isfile(rules_py):
            run_python_script(rules_py)
        else:
            print(f"[-] rules.py not found in {rules_dir}")

    print("\n[+] Done! All modules processed.")
    print("[*] Scanning MQTT broker and retrieving CVEs...")
    versionscan()
    print("[*] Generating vulnerability report PDF...")
    reportgen()

    print("[✓] Done. Report saved as mqtt_cve_report.pdf")

if __name__ == '__main__':
    main()
