CSC6410 — Experiment 3
Network Configuration Validation and Drift Detection

Project Overview:

In this experiment, I used Python, JSON, a YANG-like model, and JSON Schema to collect and check my Windows computer's network configuration.

The main purpose was to find out whether Python can collect network information faster and more accurately than manual checking.

Tools Used:

- Windows PowerShell
- Python 3.12.2
- psutil and jsonschema
- VS Code
- GitHub

Files

| File | Purpose |
|---|---|
| collect_network.py | Collects actual network settings |
| check_drift.py | Compares intended and observed settings |
| intended.json | Contains expected network settings |
| host_schema.json | Defines JSON validation rules |
| host_model.yang | Defines the network configuration model |
| observed_redacted.json | Privacy-safe example of collected data |

How to Run

Install the required Python libraries:

powershell
python -m pip install psutil jsonschema


Collect network information:

powershell
python collect_network.py


Check configuration drift:

powershell
python check_drift.py


Both scripts should be run from the folder containing the required JSON files.

Experiment Results

| Test | Result |
|---|---|
| Manual checking | 53 minutes |
| Python collection | 2.458 seconds |
| Interfaces collected | 8 |
| Original JSON validation | VALID |
| Initial drift check | No drift |
| Wi-Fi OFF | Drift detected |
| Wi-Fi restored | No drift |
| Invalid MTU test | Error detected |

During testing, I also encountered a filename mismatch and a missing comma in a JSON file. I corrected both problems and successfully continued validation.

What I Learned

I understood how Python collects network information, how JSON stores the data, and how JSON Schema checks whether the values follow the required rules.

The drift test helped me understand how changes in the actual configuration can be compared with the expected settings.

Python was much faster for collecting network information after the script was developed. However, creating and troubleshooting the script required additional time.

Privacy

The original observed.json contains private network information and is not uploaded to this repository.

The shared observed_redacted.json hides identifying network details. It is provided as a sample and is not intended to pass the original MAC-address validation rule because some MAC bytes are replaced with xx.

To reproduce the experiment, run collect_network.py on your own Windows computer to generate a local observed.json.
