# app/services/emailer.py
import smtplib, ssl
from email.message import EmailMessage

def send_report(mail_from, mail_to, smtp_host, smtp_port, smtp_user, smtp_pass, files):
    msg = EmailMessage()
    msg["Subject"] = "Backtest Reports"
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content("Attached are the generated reports.")
    for f in files:
        with open(f, "rb") as fp:
            data = fp.read()
        msg.add_attachment(data, maintype="application", subtype="pdf", filename=f)
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.starttls(context=context)
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)