import imaplib
import email
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()


# Set up your Gmail account credentials and server details
username = os.getenv("GMAIL_UID")
password = os.getenv("GMAIL_PASSWORD")
print(username, password)
imap_server = 'imap.gmail.com'

# Set up your server endpoint URL
server_url = 'http://localhost:8080/api/breakdown'

# Connect to Gmail's IMAP server
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, password)
imap.select('inbox')

# Set up a loop to continually check for new emails
while True:
    # Search for new emails in the inbox
    status, messages = imap.search(None, 'UNSEEN')

    # If there are new emails, process them
    if messages[0]:
        # Get the message IDs of the new emails
        message_ids = messages[0].split()

        for message_id in message_ids:
            # Get the raw message data for the email
            status, message_data = imap.fetch(message_id, '(RFC822)')
            raw_email = message_data[0][1]

            # Parse the raw email data into an email message object
            email_message = email.message_from_bytes(raw_email)

            # Extract the content of the email
            email_content = email_message.get_payload()

            # Send the email content to your server using an HTTP POST request
            response = requests.post(server_url, data=email_content)

            # Print the response from the server
            print(response.text)

            # Mark the email as read so it won't be processed again
            imap.store(message_id, '+FLAGS', '\\Seen')
    
    # Wait for a certain amount of time before checking for new emails again
    time.sleep(30)

# Disconnect from the IMAP server
imap.close()
imap.logout()
