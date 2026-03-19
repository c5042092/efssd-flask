# This code imports the Flask library and some functions from it.
from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from db.db import *

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

# Helper function to get a username by user ID and provide it to templates 
# eg: {{ film['user']|get_username }})
@app.template_filter()
def get_username(user_id):
    user = get_user_by_id(user_id)
    return user['username'] if user else 'Unknown'

# Routes
#===================
# These define which template is loaded, or action is taken, depending on the URL requested
#===================
# Home Page
@app.route('/')
def index():
    # This defines a variable 'studentName' that will be passed to the output HTML
    studentName = "SHU Student"
    # If a ‘username’ exists in the session data, use this instead
    if 'username' in session:
        studentName = session['username']
    # Get a list of films to display on the homepage
    films = get_all_films(limit=5, order_by='created DESC')  # Fetch the latest 5 films added
    # Render the 'index.html' template and pass the 'name' variable to it and a title to set the page title dynamically
    return render_template('index.html', title="Welcome", username=studentName, films=films)

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

        # Check if username already exists
        if get_user_by_username(username):
            error = 'Username already exists! Please choose a different one.'
        # If no errors, insert the new user
        if error is None:
            create_user(username, password)
            flash(category='success', message=f"Registration successful! Welcome {username}!")
            return redirect(url_for('login'))
        else:
            # Else, re-render the registration form with error messages
            flash(category='danger', message=f"Registration failed: {error}")
            return render_template('register.html', title="Register")

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

        # Validate user credentials
        if error is None:
            user = validate_login(username, password)
            if user is None:
                error = 'Invalid username or password!'
            else:
                session.clear()
                session['user_id'] = user['id']
                session['username'] = user['username']

        # Display appropriate flash messages
        if error is None:
            flash(category='success', message=f"Login successful! Welcome back {username}!")
            return redirect(url_for('index'))
        else:
            flash(category='danger', message=f"Login failed: {error}")

    # If the request method is GET, render the login form
    return render_template("login.html", title="Log In")

@app.route('/logout/')
def logout():
    # Clear the session and redirect to the index page with a flash message
    session.clear()
    flash(category='info', message='You have been logged out.')
    return redirect(url_for('index'))

# Films List Page
@app.route('/films/')
def films():
    user_id = session.get('user_id')  # Get the logged-in user's ID from the session
    
    # Ensure user is logged in to view films
    if user_id is None:
        flash(category='warning', message='You must be logged in to view this page.')
        return redirect(url_for('login'))
    
    # Get films list data
    film_list = get_all_films(user_id)

    # Render the films.html template with a list of films
    return render_template('films.html', title="Your Films", films=film_list, films_user=user_id)

# Film Detail Page
@app.route('/film/<int:id>/')
def film(id):
    # Get film data
    film_data = get_film_by_id(id) 
    if film_data:
        return render_template('film.html', title=film_data['title'], film=film_data)
    else:
        # If film not found, redirect to films list with a flash message
        flash(category='warning', message='Requested film not found!')
        return redirect(url_for('films'))
    
# Users Films List Page
@app.route('/films/<int:user_id>/')
def userFilms(user_id):
    
    # Get films list data
    film_list = get_all_films(user_id)  
    # Get user info
    user = get_user_by_id(user_id)
    # Render the films.html template with a list of films
    return render_template('films.html', title=f"Films added by {user['username']}", films=film_list, films_user=user_id)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    # If the request method is POST, process the form submission
    if request.method == 'POST':
        # Get the title input from the form
        title = request.form['title']
        # Validate the input
        if not title:
            flash(category='danger', message='Title is required!')
            return render_template('create.html')
        
        # [TO-DO]: Add real creation logic here (e.g. save to database record)

        new_film = {
            'user': 1, # test user
            'title': title,
            'tagline': request.form.get('tagline', ''),
            'director': request.form.get('director', ''),
            'poster': request.form.get('poster', ''),
            'release_year': request.form.get('release_year', 0),
            'genre': request.form.get('genre', ''),
            'watched': 'watched' in request.form,
            'rating': request.form.get('rating', 0),
            'review': request.form.get('review', '')
        }
        create_film(new_film)
        # ===========================
        # Flash a success message
        flash(category='success', message='Created successfully!')
        return redirect(url_for('films'))
    return render_template('create.html', title="Add A New Film")

@app.route('/update/<int:id>/', methods=('GET', 'POST'))
def update(id):
    # Get film data
    film_data = get_film_by_id(id)
    if not film_data:
        flash('Film not found!', 'warning')
        return redirect(url_for('films'))
    
    if request.method == 'POST':
        # Get the title input from the form
        title = request.form['title']
        # Validate the input
        if not title:
            flash(category='danger', message='Title is required!')
            return render_template('update.html', id=id)
        
        # [TO-DO]: Add real update logic here (e.g. update database record)

        updated_fields = {
            'title': title,
            'tagline': request.form.get('tagline', ''),
            'director': request.form.get('director', ''),
            'poster': request.form.get('poster', ''),
            'release_year': request.form.get('release_year', 0),
            'genre': request.form.get('genre', ''),
            'watched': 'watched' in request.form,
            'rating': request.form.get('rating', 0),
            'review': request.form.get('review', '')
        }
        update_film(id, updated_fields)
        # ===========================
        # Flash a success message
        flash(category='success', message='Updated successfully!')
        return redirect(url_for('film', id=id))
    return render_template('update.html', title="Update Film", film=film_data)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    # [TO-DO]: Add real deletion logic here (e.g. delete database record)
    delete_film(id)
    # ===========================
    # Flash a success message and redirect to the index page
    flash(category='success', message='Film deleted successfully!')
    return redirect(url_for('films'))


# Run application
#=========================================================
# This code executes when the script is run directly.
if __name__ == '__main__':
    print("Starting Flask application...")
    print("Open Your Application in Your Browser: http://localhost:81")
    # The app will run on port 81, accessible from any local IP address
    app.run(host='0.0.0.0', port=81, debug=True)