# This code imports the Flask library and some functions from it.
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

# Create a Flask application instance
app = Flask(__name__)

siteName = "SHU EFSSD Module"
# Set the site name in the app context
@app.context_processor
def inject_site_name():
    return dict(siteName=siteName)

app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app) # This automatically protects all POST routes
# Create the csrf_token global variable
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf())

# Routes
#===================
# These define which template is loaded, or action is taken, depending on the URL requested
#===================
# Home Page
@app.route('/')
def index():
    studentName = "Victor Abbah"
    return render_template('index.html', title="Welcome", username=studentName)

@app.route('/about')
def about():
    return render_template('about.html', title="About EFSSD")

@app.route('/about/<name>')
def aboutName(name):
    return f"<h1>About {name}!</h1><p>It is easy to create new routes</p>"

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us")

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']

        # Simple validation checks
        error = None
        if not username:
            error = 'Username is required!'
        elif not password or not repassword:
            error = 'Password is required!'
        elif password != repassword:
            error = 'Passwords do not match!'

        # Display appropriate flash messages
        if error is None:
            flash(category='success', message=f"The Form Was Posted Successfully! Well Done {username}")
        else:
            flash(category='danger', message=error)

        # [TO-DO]: Add real registration logic here (i.e., save to database)

    # If the request method is GET, just render the registration form
    return render_template('register.html', title="Register")

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Simple validation checks
        error = None
        if not username:
            error = 'Username is required!'
        elif not password:
            error = 'Password is required!'

        # [TO-DO]: Add real authentication logic here

        # Display appropriate flash messages
        if error is None:
            flash(category='success', message=f"Login successful! Welcome back {username}!")
            return redirect(url_for('index'))
        else:
            flash(category='danger', message=f"Login failed: {error}")

    # If the request method is GET, render the login form
    return render_template("login.html", title="Log In")

# Run application
#=========================================================
# This code executes when the script is run directly.
if __name__ == '__main__':
    print("Starting Flask application...")
    print("Open Your Application in Your Browser: http://localhost:81")
    # The app will run on port 81, accessible from any local IP address
    app.run(host='0.0.0.0', port=81, debug=True)