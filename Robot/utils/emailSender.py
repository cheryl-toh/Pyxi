import smtplib
from email.message import EmailMessage
import ssl

class Email:

    def __init__(self):
        self.sender_email = "pyxithecompanionbot@gmail.com"  
        self.receiver_email = "cheryltqr2907@gmail.com"   # Change: Replace with recipient's email address
        self.password = "ladc ynwe aoaj iywx"         

    def send_email(self, subject, body):
        try:
            # Create an EmailMessage object
            msg = EmailMessage()
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            msg['Subject'] = subject

            # Attach the body to the EmailMessage instance
            msg.set_content(body)

            # Create a SSL context
            context = ssl.create_default_context()

            # Connect to the SMTP server using SSL
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(self.sender_email, self.password)
                smtp.sendmail(self.sender_email, self.receiver_email, msg.as_string())

            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

# Parameters
# sender_email = "pyxithecompanionbot@gmail.com"  # Replace with your valid Gmail address
# receiver_email = "jescheoy@gmail.com"   # Replace with recipient's email address
# password = "ladc ynwe aoaj iywx"         # Replace with your Gmail account's app-specific password
# subject = "Hi bb is me pyxi"
# body = """\
# Hi bei,

# Pyxi is reminding u to drink more wottah.
# And bos luv u

# regards,
# pyxi da best roboboi
# """
# # Send the email
# send_email(sender_email, receiver_email, password, subject, body)
