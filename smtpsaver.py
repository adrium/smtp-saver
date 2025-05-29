import datetime
import email
import email.policy
import json
import os
import shlex

config = {}
with open(os.environ['SMTP_SAVER_CONFIG']) as f:
	config = json.load(f)

class Handler:
	async def handle_DATA(self, server, session, envelope):
		message = email.message_from_bytes(envelope.content, policy = email.policy.default)

		info = { k.lower(): v for k, v in message.items() }
		info['return-path'] = envelope.mail_from
		info['x-original-to'] = ','.join(envelope.rcpt_tos)
		info['now'] = datetime.datetime.now()
		print(config['log-mail'].format(**info))

		rcptconfig = config['recipients'][info['x-original-to']]

		for part in message.walk():
			fn = part.get_filename()
			if fn:
				info['filename'] = fn
				info['fullname'] = rcptconfig['fullname'].format(**info)

				content = part.get_content()
				mode = 'w' if isinstance(content, str) else 'wb'
				with open(info['fullname'], mode) as f:
					f.write(content)

				print(config['log-file'].format(**info))

				infoq = { k: shlex.quote(str(v)) for k, v in info.items() }
				os.system(rcptconfig['command'].format(**infoq))

		return '250 OK'
