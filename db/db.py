from db.test_data import films_data
import sqlite3
import os
from flask import abort
from werkzeug.security import check_password_hash, generate_password_hash

# This defines which functions are available for import when using 'from db.db import *'
__all__ = [
    "get_all_films",
    "get_film_by_id",
    "create_film",
    "update_film",
    "delete_film",
    "create_user",
    "validate_login",
    "get_user_by_username",
    "get_user_by_id",
]

# Establish connection to the SQLite database
def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
    DB_PATH = os.path.join(BASE_DIR, 'database.db') # Construct the full path to the database file
    conn = sqlite3.connect(DB_PATH)                 # Connect to the database
    conn.row_factory = sqlite3.Row                  # Enable dictionary-like access to rows
    return conn

# Authentication functions
# =========================================================
# Insert a new user (Register)
def create_user(username, password):
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, 
hashed_password))
    conn.commit()
    conn.close()
# Validate user exists with password (Login)
def validate_login(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        return user
    return None
# Check if a user exists
def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user
# Get user by ID
def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user

# Film Display functions
# =========================================================
# Get all films (or filter by user)
def get_all_films(user=None, limit=None, order_by='title ASC'):
    conn = get_db_connection()
    # Construct base query
    query = 'SELECT * FROM films'
    # If user is specified, filter films by that user
    if user:
        query += ' WHERE user = ?'
    # Add ORDER BY to the query if specified
    query += f' ORDER BY {order_by}'
    # Add LIMIT if specified
    if limit:
        query += f' LIMIT {limit}'
    # Execute the query
    if user:
        films = conn.execute(query, (user,)).fetchall()
    else:
        films = conn.execute(query).fetchall()
    conn.close()
    
    return films

# Get a film by its ID
def get_film_by_id(film_id):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM films WHERE id = ?', (film_id,)).fetchone()
    conn.close()
    return film

# Create a new film
def create_film(user_id, title, tagline, director, poster, release_year, genre, watched, 
rating, review):
    conn = get_db_connection()
    conn.execute('INSERT INTO films (user, title, tagline, director, poster, release_year, genre, watched, rating, review) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    (user_id, title, tagline, director, poster, release_year, genre, watched, rating, review))
    conn.commit()
    conn.close()

# Update a film by its ID
def update_film(film_id, title, tagline, director, poster, release_year, genre, watched, rating, review):
    conn = get_db_connection()
    conn.execute('UPDATE films SET title = ?, tagline = ?, director = ?, poster = ?, release_year = ?, genre = ?, watched = ?, rating = ?, review = ? WHERE id = ?',
    (title, tagline, director, poster, release_year, genre, watched, rating, review, film_id))
    conn.commit()
    conn.close()

# Delete a film by its ID
def delete_film(film_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM films WHERE id = ?', (film_id,))
    conn.commit()
    conn.close()
