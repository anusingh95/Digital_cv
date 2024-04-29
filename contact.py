import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from email.header import Header
from email.utils import formataddr
import streamlit as st

email = "anusingh26may@gmail.com"
receiver_email = "anusinghpu26@gmail.com"
password= st.secrets['api']['email_password']



def send_email( body, subject, sender_name):
    # MIME email parts
    msg = MIMEMultipart()
    msg["From"] = formataddr((str(Header(sender_name, 'utf-8')), email))  # Replace 'Your Name' with sender's name
    msg["To"] = receiver_email
    msg["Subject"] = str(Header(subject, 'utf-8'))  # Converting subject to a string

    msg.attach(MIMEText(body, 'plain', 'utf-8'))  # Encoding the body

    # for file_path in file_list:
    #     try:
    #         with open(file_path, 'rb') as attachment:
    #             attachment_content = attachment.read()
    #     except (FileNotFoundError, PermissionError):
    #         st.error(f"Error: Unable to open file '{file_path}'.")
    #         continue
    #     except ValueError:
    #         st.error(f"Error: File '{file_path}' contains an invalid byte.")
    #         continue

    #     attachment_package = MIMEBase('application', 'octet-stream')
    #     attachment_package.set_payload(attachment_content)
    #     encoders.encode_base64(attachment_package)
    #     attachment_package.add_header('Content-Disposition', f"attachment; filename={os.path.basename(file_path)}")
    #     msg.attach(attachment_package)

    text = msg.as_string()

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls(context=ssl.create_default_context())
    server.login(email, password)
    server.sendmail(email, receiver_email, text)
    server.quit()

            
        
        


