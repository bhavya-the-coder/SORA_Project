import os
import smtplib
from pathlib import Path
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_email():

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_APP_PASSWORD")

    receiver_emails = os.getenv("RECEIVER_EMAILS")

    if not receiver_emails:
        print("No receiver emails configured.")
        return

    recipients = [
        email.strip() for email in receiver_emails.split(",") if email.strip()
    ]

    report_path = Path("data/SORA_Report.xlsx")

    if not report_path.exists():
        print(f"Report not found: {report_path}")
        return

    msg = EmailMessage()

    msg["Subject"] = "Daily SORA Report"
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)

    msg.set_content(
        """Hi,

Please find attached today's SORA report.

Regards,
SORA Automation
"""
    )

    with open(report_path, "rb") as file:

        msg.add_attachment(
            file.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=report_path.name,
        )

    try:

        print("Connecting to Gmail...")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(
                sender_email,
                sender_password,
            )

            smtp.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:

        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    send_email()
