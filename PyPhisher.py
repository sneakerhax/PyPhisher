import smtplib
import sys, argparse
import re
import base64 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def banner():
	print "#################################"
	print "#          PyPhisher            #"
	print "#       by: sneakerhax          #"
	print "#################################"

def open_html_file(file):
	with open(file, 'r') as open_html:
		email_html = open_html.read()
	return email_html
	
def replace_links(url):
	html_regex = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\[\]]+|\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\))+(?:\(([^\s()<>\[\]]+|(\([^\s()<>\[\]]+\)))*\)|[^\s`!(){};:'".,<>?\[\]]))""")
	html_output = html_regex.sub(url, message_html)
	return html_output
			
def mime_message(subject, sendto, sender, html):
	msg = MIMEMultipart('alternative')
	msg['To'] = sendto
	msg['From'] = sender
	msg['Subject'] = subject
	message = MIMEText(html, 'html')
	msg.attach(message)
	return msg.as_string()
	
def send_email(server, port, username, password, sender, sendto, message):
	s = smtplib.SMTP(server, port)
	s.starttls()
	s.ehlo()
	s.login(username, password)
	s.sendmail(sender, sendto, message)
	s.quit()

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--server', action='store', dest='server',type=str, help='server address')
	parser.add_argument('--port', action='store', dest='port', type=int, help='server port')
	parser.add_argument('--username', action='store', dest='username', type=str, help='username')
	parser.add_argument('--password', action='store', dest='password', type=str, help='password')
	parser.add_argument('--html', action='store', dest='html', type=str, help='email html')
	parser.add_argument('--url_replace', action='store', dest='url_replace', type=str, help='url to replace')
	parser.add_argument('--subject', action='store', dest='subject', type=str, help='subject of message')
	parser.add_argument('--sender', action='store', dest='sender', type=str, help='email sender')
	parser.add_argument('--sendto', action='store', dest='sendto', type=str, help='send to address')

	args = parser.parse_args()
	
	banner()
	
	message_html = open_html_file(args.html)
	html_output = replace_links(args.url_replace)
	message = mime_message(args.subject, args.sendto, args.sender, html_output)
	send_email(args.server, args.port, args.username, args.password, args.sender, args.sendto, message)
	
