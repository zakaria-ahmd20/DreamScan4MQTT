import json
import subprocess
import os
from datetime import datetime

def reportgen():
    # Path setup
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))  # go up from scripts/
    results_dir = os.path.join(project_root, 'results')
    report_dir = os.path.join(project_root, 'reports')
    os.makedirs(report_dir, exist_ok=True)

    # Load CVE data
    with open(os.path.join(results_dir, "mqtt_cve_data.json"), "r") as f:
        raw = json.load(f)

    cves = raw["cves"]["cves"]["cves"]

    # Group CVEs by severity
    grouped = {
        "Critical (9.0–10.0)": [],
        "High (7.0–8.9)": [],
        "Medium (4.0–6.9)": [],
        "Low (0.1–3.9)": [],
        "Unscored / Unknown": []
    }

    for entry in cves:
        try:
            score = float(entry.get("cvss", 0))
        except:
            score = 0.0

        if score >= 9.0:
            group = "Critical (9.0–10.0)"
        elif score >= 7.0:
            group = "High (7.0–8.9)"
        elif score >= 4.0:
            group = "Medium (4.0–6.9)"
        elif score > 0:
            group = "Low (0.1–3.9)"
        else:
            group = "Unscored / Unknown"

        grouped[group].append(entry)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tex_path = os.path.join(report_dir, "mqtt_cve_report.tex")

    with open(tex_path, "w") as f:
        f.write(r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\title{MQTT CVE Security Report}
\date{""" + now + r"""}
\begin{document}
\maketitle

\section*{Broker Information}
\begin{itemize}
  \item \textbf{IP Address:} """ + raw["broker_ip"] + r"""
  \item \textbf{Port:} """ + str(raw["broker_port"]) + r"""
  \item \textbf{Version:} """ + raw["version_raw"].replace('_', r'\_') + r"""
  \item \textbf{CPE:} """ + raw["cpe"].replace('_', r'\_') + r"""
\end{itemize}

\section*{Executive Summary}
This report summarizes known vulnerabilities affecting the Mosquitto MQTT broker.

""")

        # CVE Count Summary
        total_cves = sum(len(v) for v in grouped.values())
        f.write(r"\textbf{Total CVEs found:} " + str(total_cves) + r"\\" + "\n")
        for severity, items in grouped.items():
            f.write(r"\quad $\bullet$ " + severity + ": " + str(len(items)) + r"\\" + "\n")
        f.write("\n")

        # Detailed CVEs
        for severity, items in grouped.items():
            if not items:
                continue

            f.write(r"\section*{" + severity + " (" + str(len(items)) + r" CVEs)}" + "\n")

            for cve in items:
                f.write(r"\textbf{CVE ID:} " + cve.get("cve_id", "UNKNOWN").replace('_', r'\_') + r"\\" + "\n")
                f.write(r"\textbf{CVSS Score:} " + str(cve.get("cvss", "N/A")) + r"\\" + "\n")
                f.write(r"\textbf{Published:} " + cve.get("published_time", "N/A") + r"\\" + "\n")

                summary = cve.get("summary", "")
                summary = summary.replace('_', r'\_').replace('%', r'\%').replace('&', r'\&').replace('#', r'\#')
                f.write(r"\textbf{Summary:} " + summary.strip().replace('\n', ' ') + r"\\" + "\n")

                refs = cve.get("references", [])
                if isinstance(refs, list) and refs:
                    f.write(r"\textbf{References:}\\\begin{itemize}" + "\n")
                    for ref in refs:
                        safe = ref.replace('_', r'\_').replace('%', r'\%').replace('&', r'\&')
                        f.write(r"\item \href{" + ref + "}{" + safe + "}" + "\n")
                    f.write(r"\end{itemize}" + "\n")

                f.write(r"\vspace{0.5cm}" + "\n")

        # Additional Tests Section
        f.write(r"\section*{Additional Tests}" + "\n")
        f.write("The following test modules were run, and here are their results:\n\n")

        excluded_files = {"mqtt_cve_data.json", "results.json"}

        for filename in os.listdir(results_dir):
            if filename.endswith(".json") and filename not in excluded_files:
                filepath = os.path.join(results_dir, filename)
                try:
                    with open(filepath, "r") as jf:
                        data = json.load(jf)

                        if isinstance(data, list):
                            for item in data:
                                test_name = item.get("test", filename.replace('.json', '')).replace('_', r'\_')
                                result_text = str(item.get("result", "No result")).replace('_', r'\_')
                                f.write(r"\textbf{Test:} " + test_name + r"\\" + "\n")
                                f.write(r"\textbf{Result:} " + result_text + r"\\" + "\n")
                                f.write(r"\vspace{0.2cm}" + "\n")

                        elif isinstance(data, dict):
                            test_name = data.get("test", filename.replace('.json', '')).replace('_', r'\_')
                            result_text = str(data.get("result", json.dumps(data))).replace('_', r'\_')
                            f.write(r"\textbf{Test:} " + test_name + r"\\" + "\n")
                            f.write(r"\textbf{Result:} " + result_text + r"\\" + "\n")
                            f.write(r"\vspace{0.2cm}" + "\n")

                except Exception as e:
                    f.write(r"\textbf{Error reading file " + filename.replace('_', r'\_') + r":} " + str(e).replace('_', r'\_') + r"\\" + "\n")

        f.write(r"\end{document}" + "\n")

    # Compile PDF
    print(f"[✓] LaTeX source written to {tex_path}")
    print("[*] Compiling PDF...")

    subprocess.run(
        ["pdflatex", "-output-directory", report_dir, tex_path],
        timeout=10
    )

    pdf_path = os.path.join(report_dir, "mqtt_cve_report.pdf")
    print(f"[✓] PDF generated: {pdf_path}")

