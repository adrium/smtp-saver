from aiosmtpd.controller import Controller
from datetime import datetime
from email import message_from_bytes
from email.header import decode_header, make_header
from os import system
from shlex import quote
from sys import argv
from time import sleep
import json

def hdrparse(s: str) -> str:
	return str(make_header(decode_header(s)))

def loadJson(file: str) -> dict:
	with open(file) as f:
		return json.load(f)

class CustomSMTPHandler:
	async def handle_DATA(self, server, session, envelope):
		msg = message_from_bytes(envelope.content)
		info = { k.lower(): hdrparse(v) for k, v in msg.items() }
		info['now'] = datetime.now()
		info['return-path'] = envelope.mail_from
		info['x-original-to'] = envelope.rcpt_tos[0]
		print(config['log-mail'].format(**info))
		if (info['x-original-to'] in config['recipients']):
			rcptconfig = config['recipients'][info['x-original-to']]
			for part in msg.walk():
				fn = part.get_filename()
				if fn:
					info['filename'] = hdrparse(fn)
					info['fullname'] = rcptconfig['fullname'].format(**info)
					print(config['log-file'].format(**info))
					with open(info['fullname'], 'wb') as f:
						f.write(part.get_payload(decode = True))
					system(rcptconfig['command'] + ' ' + quote(info['fullname']))
		else:
			print('No config for: ' + info['x-original-to'])
		return '250 OK'

config = loadJson(argv[1])
handler = CustomSMTPHandler()
server = Controller(handler = handler, hostname = config['host'], port = config['port'])
server.start()
while True:
	sleep(30)
