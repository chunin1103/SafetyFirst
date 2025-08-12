import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for

# Create an instance of the Flask class
app = Flask(__name__)

# --- Function to send email notification (No changes needed) ---
def send_notification_email(new_email):
    """Sends an email notification when a new user signs up."""
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')

    if not sender_email or not sender_password:
        print("Error: Email credentials are not set as secrets.")
        return

    receiver_email = sender_email
    msg = MIMEMultipart()
    msg['Subject'] = "🎉 New Waitlist Signup!"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    body = f"A new user has signed up for the waitlist:\n\n{new_email}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Notification email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # Just send the email and log it. No database.
            send_notification_email(email)
            print(f"Notification email sent for: {email}")
        
        # Always redirect to the thank you page after a POST request
        return redirect(url_for('thank_you'))

    # For GET requests, just show the homepage
    return render_template('index.html')


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# This part is for local testing and doesn't affect production on Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)