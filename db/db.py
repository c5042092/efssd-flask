from db.test_data import films_data
# Placeholder functions to simulate database operations
# Get all films
def get_all_films():
    return films_data
    # Get a film by its ID
    def get_film_by_id(film_id):
        return next((film for film in films_data if film['id'] == film_id), None)

# Get a film by its ID
def get_film_by_id(film_id):
    return next((film for film in films_data if film['id'] == film_id), None)

def create_film(film_data):
    # Generate a new ID based on the current max
    new_id = max(f['id'] for f in films_data) + 1 if films_data else 1
    film_data['id'] = new_id
    films_data.append(film_data)
    return film_data

# Update an existing film
def update_film(film_id, updated_data):
    film = get_film_by_id(film_id)
    if film:
        film.update(updated_data)
        return film
    return None

# Delete a film by its ID
def delete_film(film_id):
    films_data.pop(film_id-1)
    return
