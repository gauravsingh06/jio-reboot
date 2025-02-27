
![Untitled design (4)](https://github.com/user-attachments/assets/5b94cc96-e12b-4149-96ec-34385afa460f)
# Jio Router Reboot
Simple script to reboot your Jio Router remotely or automatically, even if you're too lazy to unplug and replug the adapter. Effortless network reset in a few lines of code.

## Installation

```bash
pip install git+https://github.com/gauravsingh06/jio-reboot.git
```

## Usage

```bash
# First time running will prompt for credentials
jioreboot

# To reconfigure your router credentials
jioreboot --configure

# See all available options
jioreboot --help

# Enable debug mode
jioreboot --debug
```

## Uninstallation

To remove this package, first ensure it is installed. You can check the installed packages with:

```bash
pip list
```

If `jioreboot` is listed, you can uninstall it with the following command:

```bash
pip uninstall jioreboot
```

## Features

- Securely saves router credentials for future use
- Fixed URL for the JioFiber router (http://192.168.29.1/platform.cgi)
- Command-line options to override saved username and password
- Reconfiguration option to update saved settings
- Color-coded output for better readability

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- urllib3
