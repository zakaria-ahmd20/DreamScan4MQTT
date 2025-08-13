# DreamScan4MQTT – MQTT Broker Vulnerability Scanner

Dream4MQTT is a Dynamic Rule-Based Vulnerabil-ity Scanner for MQTT Brokers devoloped in python3 tested for Mosquitto Brokers.
## Features

- Detects Vulnerabalties and misconfigs
- Retrieves CVEs from public databases based on version number
- Performs authentication bypass checks
- Modular test architecture (easily extensible)
- Fingerprinting module avalible for version 1.3.1-.13.5
- Generates a detailed PDF vulnerability report via LaTeX

## Requirements

### Python3 Dependencies

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
## Running the Scanner
A config file can be found containing the IP and Port of the broker in /Dreamscan4MQTT/config/config.json
Please edit according to the target IP address and Port
```bash
{
  "broker_ip": "192.168.15.211",
  "broker_port": 1883
}
## Testing the Scanner

To quickly test DreamScan 4MQTT, you can run a Mosquitto broker using the pre-built Docker image:

```bash
# Pull the Docker image
docker pull zahmed70/mosquitto-1.3.1:latest

# Run the broker on default MQTT port 1883
docker run -it -p 1883:1883 -v ~/mosquitto/config:/mosquitto/config zahmed70/mosquitto-1.3.1
```
Use the following config file for testing the python tool

```bash
listener 1883
user root
allow_anonymous true

```

## Example Output

```
[*] Scanning MQTT broker and retrieving CVEs...
Raw Broker Version: mosquitto version 2.0.16
Detected Version: 2.0.16
CPE: cpe:2.3:a:eclipse:mosquitto:1.3.1:*:*:*:*:*:*:*
[✓] LaTeX source written to reports/mqtt_cve_report.tex
[*] Compiling PDF...
[✓] Report generated: reports/mqtt_cve_report.pdf
```

## Troubleshooting

- Missing LaTeX packages: install `texlive-latex-extra` if you see errors
- PDF compilation timeout: increase timeout in `generate_report.py`
- Python module not found (`rule_engine` or `paho-mqtt`): `pip3 install paho-mqtt rule-engine`

## Notes

- DreamScan4MQTT is designed for research and testing on brokers you own or have permission to scan.
- Please use within the legal frameworks of your country and be ethical :)
- The scanner is modular; we advise you to add new modules as alot of work is there to be done.

## License

MIT License
