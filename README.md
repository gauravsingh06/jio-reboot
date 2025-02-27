# Router Reboot

A simple command-line utility to reboot JioFiber routers.

## Installation

```bash
pip install -e .
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

To remove this package, run the following command:

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
