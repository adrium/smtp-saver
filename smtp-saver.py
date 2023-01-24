from aiosmtpd.controller import Controller
from email import message_from_bytes
from email.header import decode_header, make_header

class CustomSMTPHandler:
	async def handle_DATA(self, server, session, envelope):
		msg = message_from_bytes(envelope.content)
		headers = { k.lower(): str(make_header(decode_header(v))) for k, v in msg.items() }
		headers['mail_from'] = envelope.mail_from
		headers['rcpt_tos'] = envelope.rcpt_tos
		print(headers)
		for part in msg.walk():
			fn = part.get_filename()
			if fn:
				fn = str(make_header(decode_header(fn)))
				print('Saving ' + fn)
				with open(fn, 'wb') as f:
					f.write(part.get_payload(decode = True))
		return '250 OK'

handler = CustomSMTPHandler()
server = Controller(handler = handler, hostname = '127.0.0.1')
server.start()
while True:
	input()
