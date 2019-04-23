#!/usr/bin/env python3
import os
import smtplib
import sys
from pathlib import Path
import email.encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from io import StringIO
from argparse import ArgumentParser


def create_message(cert_dir, domains, mail_from, mail_to):
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

    return msg


def main():
    parser = ArgumentParser(description="Send email notification about renewed certificates.")
    parser.add_argument('mail_from')
    parser.add_argument('mail_to')
    parser.add_argument('--print-only', action='store_true', default=False,
                        help="Only print the email to stdout; do not send anything")
    parser.add_argument('--smtp-host', default="localhost", help="SMTP host for sending mails")
    parser.add_argument('--smtp-port', default="25", type=int, help="SMTP port for sending mails")

    options = parser.parse_args()

    mail_from = options.mail_from
    mail_to = options.mail_to

    domains = os.environ['RENEWED_DOMAINS'].split()
    cert_dir = Path(os.environ['RENEWED_LINEAGE'])

    msg = create_message(cert_dir, domains, mail_from, mail_to)

    if options.print_only:
        sys.stdout.buffer.write(msg.as_bytes())
    else:
        with smtplib.SMTP(options.smtp_host, port=options.smtp_port) as server:
            try:
                server.starttls()
                server.ehlo()
            except smtplib.SMTPException:
                pass
            server.send_message(msg)


if __name__ == "__main__":
    main()