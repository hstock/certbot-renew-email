#!/bin/env python3
import os
import smtplib
import sys
from pathlib import Path
import email.encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from io import StringIO


def main():
    mail_from = sys.argv[1]
    mail_to = sys.argv[2]

    domains = os.environ['RENEWED_DOMAINS'].split()
    cert_dir = Path(os.environ['RENEWED_LINEAGE'])

    msg = MIMEMultipart()
    msg['Subject'] = 'Certificate Update for {}'.format(', '.join(domains))
    msg['From'] = mail_from
    msg['To'] = mail_to

    content = StringIO()
    print("A new certificate has been issued for the following domains:\n", file=content)
    for domain in domains:
        print("* {}".format(domain), file=content)
    print("\nThe new certificate is attached to this E-Mail.\n\nGreetings,\n\nyour IT-Team", file=content)

    msg.attach(MIMEText(content.getvalue()))

    with open(str(cert_dir / 'cert.pem'), 'rb') as cert:
        attachment = MIMEApplication(cert.read(), "x-pem-file", email.encoders.encode_7or8bit)
        attachment["Content-Disposition"] = "attachment; filename=cert.pem"
        msg.attach(attachment)

    print(msg.as_string())

if __name__ == "__main__":
    main()