# This code imports the Flask library and some functions from it.
from flask import Flask, render_template
# Create a Flask application instance
app = Flask(__name__)

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
    return f"<h1>About Flask!</h1><p>It is easy to create new routes</p>"

@app.route('/about/<name>')
def aboutName(name):
    return f"<h1>About {name}!</h1><p>It is easy to create new routes</p>"

# Run application
#=========================================================
# This code executes when the script is run directly.
if __name__ == '__main__':
    print("Starting Flask application...")
    print("Open Your Application in Your Browser: http://localhost:81")
    # The app will run on port 81, accessible from any local IP address
    app.run(host='0.0.0.0', port=81, debug=True)