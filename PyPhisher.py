import smtplib
import getpass
import sys
import argparse
import re
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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


def main(args):
    phish(args)


def phish(args):
    message_html = open_html_file(args.html)
    html_output = replace_links(args.url_replace, message_html)
    message = mime_message(args.subject, args.sendto, args.sender, html_output)
    send_email(args.server, args.port, args.username, args.password, args.sender, args.sendto, message)


def open_html_file(file):
    with open(file, 'r') as open_html:
        email_html = open_html.read()
    return email_html


def replace_links(url, message):
    html_regex = re.compile(r'href=[\'"]?([^\'" >]+)')
    html_output = html_regex.sub("href=\"{}".format(url), message)
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
    print("[+] Attempting to send mail")
    s.sendmail(sender, sendto, message)
    print("[+] Done...")
    s.quit()


if __name__ == '__main__':
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', required='True', action='store', dest='server', type=str, help='server address')
    parser.add_argument('--port', required='True', action='store', dest='port', type=int, help='server port')
    parser.add_argument('--username', action='store', dest='username', type=str, help='username')
    parser.add_argument('--password', action='store', dest='password', type=str, help='password')
    parser.add_argument('--html', required='True', action='store', dest='html', type=str, help='email html')
    parser.add_argument('--url_replace', action='store', dest='url_replace', type=str, help='url to replace')
    parser.add_argument('--subject', action='store', dest='subject', type=str, help='subject of message')
    parser.add_argument('--sender', action='store', dest='sender', type=str, help='email sender')
    parser.add_argument('--sendto', action='store', dest='sendto', type=str, help='send to address')
    parser.add_argument('--start-tls', action='store_true', dest='starttls', help='run using STARTTLS')

    args = parser.parse_args()

    main(args)
