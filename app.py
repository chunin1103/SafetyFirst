from flask import Flask, render_template, request, redirect, url_for

# Create an instance of the Flask class
app = Flask(__name__)

# This list will act as our temporary database to store emails
waitlist_emails = []

# Define a route for the homepage that accepts both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def home():
    # If the form is submitted (POST request)
    if request.method == 'POST':
        # Get the email from the form data
        email = request.form['email']
        
        # Add the email to our list (if it's not already there)
        if email and email not in waitlist_emails:
            waitlist_emails.append(email)
            # Print the list to the terminal to see the new entry
            print("Current Waitlist:", waitlist_emails)
        
        # Redirect the user to the 'thank you' page
        return redirect(url_for('thank_you'))
    
    # If it's a regular page visit (GET request), just show the page
    return render_template('index.html')

# Define a new route for the thank you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


# This allows you to run the app directly with 'python app.py'
if __name__ == '__main__':
    app.run(debug=True)
