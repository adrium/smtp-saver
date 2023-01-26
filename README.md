# SMTP Saver

This simple script saves all attachments received via email and executes a shell script.

The purpose is to easily save PDFs over the network obtained from a scanner/printer.

## Installation

Install script dependencies:

```
python3 -m venv /path/to/script/.venv
/path/to/script/.venv/bin/pip install aiosmtpd
cp smtp-saver.py /path/to/script
```

Copy [config.example.json](config.example.json) and save to the desired location, e.g `/path/to/config/smtp-saver.json`

Adjust [smtp-saver.service](smtp-saver.service) and place to `/etc/systemd/system`

Start script:

```
systemctl daemon-reload
systemctl start smtp-saver
systemctl enable smtp-saver
```
