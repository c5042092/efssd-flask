# This code imports the Flask library and some functions from it.
from flask import Flask, render_template
# Create a Flask application instance
app = Flask(__name__)

siteName = "SHU EFSSD Module"
# Set the site name in the app context
@app.context_processor
def inject_site_name():
    return dict(siteName=siteName)

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

# Run application
#=========================================================
# This code executes when the script is run directly.
if __name__ == '__main__':
    print("Starting Flask application...")
    print("Open Your Application in Your Browser: http://localhost:81")
    # The app will run on port 81, accessible from any local IP address
    app.run(host='0.0.0.0', port=81, debug=True)