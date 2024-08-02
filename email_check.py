import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
import time  # Import time module for delay
from datetime import datetime
import schedule

# Email account credentials
username = "aasishkrsahoo.19097@gmail.com"
password = "sgqj xpom favc ahtn"  # Replace with your app password

def get_today_date():
    # Get today's date in the format required by IMAP
    return datetime.now().strftime("%d-%b-%Y")

def check_new_emails():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")

        today_date = get_today_date()
        status, messages = mail.search(None, f'(FROM "SOA PLACEMENT CELL" SINCE {today_date})')
        print(status)
        email_ids = messages[0].split()
        print("emal_ids:",email_ids)
        if not email_ids:
            mail.logout()
            return []

        new_emails = []
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    body_= msg.get("body")
                    new_emails.append({"subject": subject, "from": from_,"body":body_})
                    print(new_emails)
        
        mail.logout()
        return new_emails
    except Exception as e:
        print(f"Error checking new emails: {e}")
        return []

def send_notification(new_emails):
    if not new_emails:
        return
    
    subject = "New Emails from Specific Senders"
    body = "\n".join(f"From: {email['from']}\nSubject: {email['subject']}\n" for email in new_emails)
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = 'aasish6001@gmail.com,zoro1080pheonix@gmail.com'
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(username, password)  # Use the app password here
            server.send_message(msg)
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Error sending notification: {e}")

def main():
    while True:
        new_emails = check_new_emails()
        send_notification(new_emails)
        print(f"Checked for new emails. Waiting for next check...")
        time.sleep(5)  # Wait for one hour

if __name__ == "__main__":
    send_notification(check_new_emails())
    # main()
    
    # schedule.every().day.at("20:34").do(main)
    # # print(schedule.every().day.at("20:36").do(main))
    # schedule.run_pending()
    # # print(schedule.run_pending())
    # # print("run")
    # # main()
    # counter =0
    # while True:
    #     if counter == 1:
    #         break
    #     schedule.run_pending()
    #     print("Schedule Ran Once")
    #     counter+=1