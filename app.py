from flask import Flask, render_template, request, redirect, url_for
import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv() # --- NEW: Load variables from .env file ---

# Create an instance of the Flask class
app = Flask(__name__)

# This list will act as our temporary database to store emails
waitlist_emails = []

# --- Function to send email notification (No changes needed here) ---
def send_notification_email(new_email):
    """Sends an email notification when a new user signs up."""
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    
    if not sender_email or not sender_password:
        print("Error: Email credentials are not set in environment variables.")
        return

    receiver_email = sender_email
    
    # --- Create a proper email structure that supports UTF-8 ---
    msg = MIMEMultipart()
    msg['Subject'] = "🎉 New Waitlist Signup!"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Define the body of the email
    body = f"A new user has signed up for the waitlist:\n\n{new_email}"
    
    # Attach the body to the email message, specifying UTF-8 encoding
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            # Send the message by converting the message object to a string
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Notification email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Define a route for the homepage that accepts both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email']
        
        if email and email not in waitlist_emails:
            waitlist_emails.append(email)
            print("Current Waitlist:", waitlist_emails)
            send_notification_email(email)
        
        return redirect(url_for('thank_you'))
    
    return render_template('index.html')

# Define a new route for the thank you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


# This allows you to run the app directly with 'python app.py'
if __name__ == '__main__':
    app.run(debug=True)