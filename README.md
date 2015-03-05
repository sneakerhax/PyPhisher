# PyPhisher

A simple python tool for phishing

## Description
This tool was created for the purpose of phishing during a penetration test. I wanted it to be a command line tool(to allow for automation) that would take a pre-crafted html email file then replace all the links and send the email. 

## Usage
```
PyPhisher.py --server <smtp server name> --port (smtp port> --username <username> --password <password> --html <file with pre-crafted html> --url_replace <the url you would like to replace all links with> --subject <email subject> --sender <sender of the mail(you may put any sender)> --sendto <who to send the message to>
```
