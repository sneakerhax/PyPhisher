# PyPhisher

A simple python tool for phishing

## Description:
This tool was created for the purpose of phishing during a penetration test. I wanted to create command line tool(to allow for automation) that would take a pre-crafted html email file then replace all the links and send the email. The replacing of links was something I was previously doing manually. This was inspired by SpearPhiser beta by Dave Kennedy from Trustedsec and a feature found in Cobalt Strike by Rapheal Mudge from Strategic Cyber

## Usage:
```
PyPhisher.py --server <smtp server name> --port <smtp port> --username <username> --password <password> --html <file with pre-crafted html> --url_replace <the url you would like to replace all links with> --subject <email subject> --sender <sender of the mail(you may put any sender)> --sendto <who to send the message to>
```
## Available options:
```
--server          The SMTP server that you are going to be using to send the email
--port            The port number that is setup for SMTP
--html            The pre-crafted html that will be used in the email
--url_replace     The url that will be used to replace all links in the email
--subject         The subject that will appear in the email message
--sender          The sender that will appear on the email example
--sendto          Who you would like to send the message to
```
