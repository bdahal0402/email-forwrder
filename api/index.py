import os
from flask import Flask, request, abort, jsonify
import smtplib

app = Flask(__name__)

# Retrieve the authentication token from the environment variable
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

# Retrieve the SFTP credentials from the environment variables
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'outlook.office365.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

@app.before_request
def authenticate():
    # Retrieve the token from the request headers
    token = request.headers.get('Authorization')

    # Check if the token matches the expected token
    if token != 'Token {}'.format(AUTH_TOKEN):
        # Token is invalid, abort the request with a 401 Unauthorized status code
        abort(401)

@app.route('/send-email', methods=['POST'])
def send_email():
    sender_email = SMTP_USERNAME
    to = request.form.get('to')
    subject = request.form.get('subject')
    body = request.form.get('body')
    cc = request.form.get('cc', '')
    bcc = request.form.get('bcc', '')

    try:
        # Create a secure connection to the mail server
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        # Start TLS encryption
        smtp.starttls()

        # Login to the sender's email account
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Create the email message
        email_message = 'Subject: {}\n'.format(subject)
        email_message += 'To: {}\n'.format(to)
        if cc:
            email_message += 'Cc: {}\n'.format(cc)
        if bcc:
            email_message += 'Bcc: {}\n'.format(bcc)
        email_message += '\n{}'.format(body)

        # Send the email
        smtp.sendmail(sender_email, to, email_message)

        # Close the SMTP connection
        smtp.quit()

        # Email sent successfully, return 200 status code
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        # Something went wrong, return 400 status code
        return jsonify({'message': str(e)}), 400

