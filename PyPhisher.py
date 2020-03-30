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
    print("    ____        ____  __    _      __")
    print("   / __ \__  __/ __ \/ /_  (_)____/ /_  ___  _____")
    print("  / /_/ / / / / /_/ / __ \/ / ___/ __ \/ _ \/ ___/")
    print(" / ____/ /_/ / ____/ / / / (__  ) / / /  __/ /")
    print("/_/    \__, /_/   /_/ /_/_/____/_/ /_/\___/_/")
    print("      /____/")
    print("")
    print("by: sneakerhax")
    print("")


def phish(args):
    message_html = open_html_file(args.html)
    html_output = replace_links(args.url_replace, message_html)
    attachment = None
    if args.attachment:
        if os.path.isfile(args.attachment):
            attachment = add_attachment(args.attachment)
    message = mime_message(args.subject, args.sendto, args.sender, html_output, attachment)
    if args.sendto:
        send_email(args.server, args.port, args.username, args.password, args.sender, args.sendto, message)
    elif args.list_sendto:
        if not os.path.isfile(args.list_sendto):
            print("[!] Invalid file {0}".format(args.list_sendto))
            sys.exit()
        handler = open(args.list_sendto, "r")
        sendtos = handler.read().splitlines()
        handler.close()
        for sendto in sendtos:
            send_email(args.server, args.port, args.username, args.password, args.sender, sendto.strip(), message)
    else:
        print("[!] You must either submit a dest mail address or a list of dests")


def open_html_file(file):
    with open(file, 'r') as open_html:
        email_html = open_html.read()
    return email_html


def replace_links(url, message):
    html_regex = re.compile(r'href=[\'"]?([^\'" >]+)')
    html_output = html_regex.sub("href=\"{}".format(url), message)
    return html_output


def mime_message(subject, sendto, sender, html, attachment):
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
        "attachment; filename={}".format(attachment),
    )
    encoders.encode_base64(part)
    return part


def get_mime_type(attachment):
    mime = magic.Magic(mime=True)
    return mime.from_file(attachment)


def send_email(server, port, username, password, sender, sendto, message):
    print("[+] Attempting to connect to server")
    s = smtplib.SMTP(server, port)
    if args.starttls:
        print("[+] Attempting to use STARTTLS")
        s.starttls()
    print("[+] Attempting to say ehlo")
    s.ehlo()
    if args.username is not None:
        print("[+] Attempting to Authenticate")
        if args.password is None:
            password = getpass.getpass("Password for {}:".format(username))
        s.login(username, password)
    print("[+] Sending mail to {0}".format(sendto))
    s.sendmail(sender, sendto, message)
    print("[+] Done...")
    s.quit()


if __name__ == '__main__':
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
