# Dream4MQTT – MQTT Broker Vulnerability Scanner

Dream4MQTT is a Python-based, modular vulnerability scanner for MQTT brokers. It fingerprints the broker version, checks authentication rules, retrieves CVEs, and generates a detailed vulnerability report in PDF format using LaTeX.

## Features

- Detects MQTT broker version and CPE
- Retrieves relevant CVEs from local or online databases
- Performs authentication bypass checks
- Modular test architecture (easily extensible)
- Generates a detailed PDF vulnerability report via LaTeX

## Requirements

### Python Dependencies

Install required Python libraries:

```bash
pip3 install paho-mqtt rule-engine
```

### LaTeX (for PDF report generation)

Dream4MQTT uses PdfLaTeX to compile the vulnerability report. On Linux (Debian/Ubuntu/Kali), run:

```bash
sudo apt update
sudo apt install texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra
```

## Testing the Scanner

To quickly test Dream4MQTT, you can run a Mosquitto broker using the pre-built Docker image:

```bash
# Pull the Docker image
docker pull zahmed70/mosquitto-1.3.1:latest

# Run the broker on default MQTT port 1883
docker run -it -p 1883:1883 -v ~/mosquitto/config:/mosquitto/config zahmed70/mosquitto-1.3.1
```

Once the broker is running, you can scan it with Dream4MQTT:

```bash
python3 main.py
```

## Example Output

```
[*] Scanning MQTT broker and retrieving CVEs...
Raw Broker Version: mosquitto version 2.0.16
Detected Version: 2.0.16
CPE: cpe:2.3:a:eclipse:mosquitto:2.0.16:*:*:*:*:*:*:*
[✓] LaTeX source written to reports/mqtt_cve_report.tex
[*] Compiling PDF...
[✓] Report generated: reports/mqtt_cve_report.pdf
```

## Troubleshooting

- Missing LaTeX packages: install `texlive-latex-extra` if you see errors
- PDF compilation timeout: increase timeout in `generate_report.py`
- Python module not found (`rule_engine` or `paho-mqtt`): `pip3 install paho-mqtt rule-engine`

## Notes

- Dream4MQTT is designed for research and testing on brokers you own or have permission to scan.
- The scanner is modular; you can add new tests or rules in the modules folder.

## License

MIT License
