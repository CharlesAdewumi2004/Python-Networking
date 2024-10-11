import smtplib  # Module for sending emails using Simple Mail Transfer Protocol (SMTP)
from email import encoders  # Module to encode attachments before sending
from email.mime.text import MIMEText  # Class to create a plain text email body
from email.mime.base import MIMEBase  # Base class for handling attachments
from email.mime.multipart import MIMEMultipart  # Class to handle multipart emails (text + attachments)

# Set up the server connection with Gmail's SMTP server using port 587 (for TLS encryption)
server = smtplib.SMTP('smtp.gmail.com', 587)

# 'ehlo()' is used to identify the server to the SMTP server.
# It tells the SMTP server that the client is ready to communicate
server.ehlo()

# Start TLS (Transport Layer Security) encryption to secure the connection
# TLS ensures that the email and login credentials are sent securely
server.starttls()

# Log in to the Gmail account using your email and app password.
# An app password is needed if 2-step verification is enabled on your account.
server.login('charlesadewumi2004@gmail.com', 'bimu ickt boix lbfz')  # Replace with your generated app password

# Create a MIMEMultipart email object, which allows us to combine the email body and attachments
msg = MIMEMultipart()

# Set the sender's email address
msg['From'] = 'charlie'  # This can be a name or the email address itself

# Set the recipient's email address
msg['To'] = 'charlesadewumi2004@gmail.com'  # Email will be sent to this address

# Set the subject of the email
msg['Subject'] = 'kappa123'  # Example subject line

# Read the content of a text file (assuming the file 'text.txt' exists in the same directory)
# This will be used as the email body.
with open('text.txt', 'r') as f:
    message = f.read()  # Read the content of the file into a variable

# Attach the content of the text file as a plain text email body
msg.attach(MIMEText(message, 'plain'))

# Convert the entire email (including body and attachments, if any) to a string format
text = msg.as_string()

# Send the email from the sender to the recipient
# Parameters: sender email, recipient email, and the email content as a string
server.sendmail('charlesadewumi2004@gmail.com', 'charlesadewumi2004@gmail.com', text)

# Close the connection to the SMTP server once the email has been sent
server.quit()



