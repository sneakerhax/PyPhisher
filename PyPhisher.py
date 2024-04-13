import re
import os
import sys
import magic
import smtplib
import getpass
import argparse
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def banner():
    banner_text = """
    ____        ____  __    _      __
   / __ \__  __/ __ \/ /_  (_)____/ /_  ___  _____
  / /_/ / / / / /_/ / __ \/ / ___/ __ \/ _ \/ ___/
 / ____/ /_/ / ____/ / / / (__  ) / / /  __/ /
/_/    \__, /_/   /_/ /_/_/____/_/ /_/\___/_/
      /____/

by: sneakerhax
"""
    print(banner_text)

def phish(args):
    message_html = open_html_file(args.html)
    html_output = replace_links(args.url_replace, message_html)
    attachment = None
    if args.attachment:
        if os.path.isfile(args.attachment):
            attachment = add_attachment(args.attachment)
    message = create_mime_message(args.subject, args.sendto, args.sender, html_output, attachment)
    if args.sendto:
        send_email(args.server, args.port, args.username, args.password, args.sender, args.sendto, message, args.starttls)
    elif args.list_sendto:
        send_to_list(args, message)
    else:
        print("[!] You must either submit a destination email address or a list of destinations")

def open_html_file(file):
    with open(file, 'r') as open_html:
        email_html = open_html.read()
    return email_html

def replace_links(url, message):
    html_regex = re.compile(r'href=[\'"]?([^\'" >]+)')
    html_output = html_regex.sub("href=\"{}".format(url), message)
    return html_output

def create_mime_message(subject, sendto, sender, html, attachment):
    msg = MIMEMultipart('alternative')
    msg['To'] = sendto
    msg['From'] = sender
    msg['Subject'] = subject
    message = MIMEText(html, 'html')
    msg.attach(message)
    if attachment is not None:
        msg.attach(attachment)
    return msg.as_string()

def add_attachment(attachment):
    mime_type_major, mime_type_minor = get_mime_type(attachment).split("/")
    with open(attachment, "rb") as f:
        part = MIMEBase(mime_type_major, mime_type_minor)
        part.set_payload(f.read())
    part.add_header(
        "Content-Disposition",
        "attachment; filename={}".format(os.path.basename(attachment)),
    )
    encoders.encode_base64(part)
    return part

def get_mime_type(attachment):
    mime = magic.Magic(mime=True)
    return mime.from_file(attachment)

def send_email(server, port, username, password, sender, sendto, message, use_starttls):
    print("[+] Attempting to connect to server")
    s = smtplib.SMTP(server, port)
    if use_starttls:
        print("[+] Attempting to use STARTTLS")
        s.starttls()
    print("[+] Attempting to say ehlo")
    s.ehlo()
    if username:
        print("[+] Attempting to Authenticate")
        if password is None:
            password = getpass.getpass("Password for {}:".format(username))
        s.login(username, password)
    print("[+] Sending mail to {0}".format(sendto))
    s.sendmail(sender, sendto, message)
    print("[+] Done...")
    s.quit()

def send_to_list(args, message):
    if not os.path.isfile(args.list_sendto):
        print("[!] Invalid file {0}".format(args.list_sendto))
        sys.exit()
    with open(args.list_sendto, "r") as handler:
        sendtos = handler.read().splitlines()
    for sendto in sendtos:
        send_email(args.server, args.port, args.username, args.password, args.sender, sendto.strip(), message, args.starttls)

def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', required=True, action='store', dest='server', type=str, help='server address')
    parser.add_argument('--port', required=True, action='store', dest='port', type=int, help='server port')
    parser.add_argument('--username', action='store', dest='username', type=str, help='username')
    parser.add_argument('--password', action='store', dest='password', type=str, help='password')
    parser.add_argument('--html', required=True, action='store', dest='html', type=str, help='email html')
    parser.add_argument('--url_replace', action='store', dest='url_replace', type=str, help='url to replace')
    parser.add_argument('--subject', required=True, action='store', dest='subject', type=str, help='subject of message')
    parser.add_argument('--sender', required=True,  action='store', dest='sender', type=str, help='email sender')
    parser.add_argument('--sendto', action='store', dest='sendto', type=str, help='send to address')
    parser.add_argument('--start-tls', action='store_true', dest='starttls', help='run using STARTTLS')
    parser.add_argument('--list-sendto', dest="list_sendto", help="List of email addresses")
    parser.add_argument('--attachment', dest='attachment', help="File to attach to the mail")
    args = parser.parse_args()

    phish(args)

if __name__ == '__main__':
    main()
