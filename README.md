# DreamScan4MQTT – MQTT Broker Vulnerability Scanner

DreamScan4MQTT is a Dynamic Rule-Based Vulnerability Scanner for MQTT Brokers developed in Python3. It has been tested for Mosquitto brokers.

## Features

- Detects vulnerabilities and misconfigurations
- Retrieves CVEs from public databases based on version number
- Performs authentication bypass checks
- New modules being added each week
- Fingerprinting module available for Mosquitto versions 1.3.1 to 1.3.5
- Generates a detailed PDF vulnerability report via LaTeX

## Requirements

### Python3 Dependencies

Install required Python libraries:

```bash
pip3 install paho-mqtt rule-engine
```

### LaTeX (for PDF report generation)

DreamScan4MQTT uses PdfLaTeX to compile the vulnerability report. On Linux (Debian/Ubuntu/Kali), run:

```bash
sudo apt update
sudo apt install texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra
```

## Running the Scanner

A configuration file is located at `/DreamScan4MQTT/config/config.json`. Edit it with the target broker's IP address and port:

```json
{
  "broker_ip": "192.168.15.211",
  "broker_port": 1883
}
```

## Testing the Scanner

To test DreamScan4MQTT, you can run a Mosquitto broker using the pre-built Docker image:

```bash
# Pull the Docker image
docker pull zahmed70/mosquitto-1.3.1:latest

# Run the broker on default MQTT port 1883
docker run -it -p 1883:1883 -v ~/mosquitto/config:/mosquitto/config zahmed70/mosquitto-1.3.1
```

### Docker Configuration

Create the directory and configuration file inside `~/mosquitto/config`:

```bash
mkdir -p ~/mosquitto/config
cd ~/mosquitto/config
```

Create `mosquitto.conf` with the following contents using a text editor:

```bash
listener 1883
user root
allow_anonymous true
```

After setting up the broker, run the scanner:

```bash
python3 main.py
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
Always cleanup before running the script twice , you can see the command below on how to cleanup
```bash
python3 scripts/cleanup.py
```
## Troubleshooting

- latex compile errors means , missing LaTeX packages: install `texlive-latex-extra` if you see error
- Python module not found (`rule_engine` or `paho-mqtt`): `pip3 install paho-mqtt rule-engine`
  

## Notes

- DreamScan4MQTT is intended for research and testing on brokers you own or have permission to scan.
- Use the tool ethically and within legal frameworks.
- The scanner is modular; you can add new modules to extend functionality.

## License

MIT License
