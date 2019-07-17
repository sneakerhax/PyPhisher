# PyPhisher

A simple python tool for phishing

### Description:
This tool was created for the purpose of phishing during a penetration test. I wanted to create command line tool(to allow for automation) that would take a pre-crafted html email file then replace all the links and send the email. The replacing of links was something I was previously doing manually. This was inspired by SpearPhiser beta by Dave Kennedy from Trustedsec and a feature found in Cobalt Strike by Rapheal Mudge from Strategic Cyber

### Usage:
```
PyPhisher.py --server mail.server.com --port 25 --username user --password password --html phish.txt --url_replace phishlink.com --subject Read!! --sender important@phish.com --sendto target@company.com
```
### Available options:
```
--server          The SMTP server that you are going to be using to send the email
--port            The port number that is setup for SMTP
--html            The pre-crafted html that will be used in the email
--url_replace     The url that will be used to replace all links in the email
--subject         The subject that will appear in the email message
--sender          The sender that will appear on the email example
--sendto          Who you would like to send the email to
--start-tls       Will attempt to upgrade connection using SSL/TLS
```

### Checking SMTP creds:

If you need to check your credentials for your SMTP server use:

https://github.com/sneakerhax/Python-Network-Tools/blob/master/scripts/smtp_authcheck.py
