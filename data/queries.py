from data import data_manager


def get_shows(page):
    return data_manager.execute_select(f"""SELECT s.id, s.title, to_char(s.year, 'YYYY') AS year, s.runtime, to_char(s.rating::float, '999.9') AS rating, 
        string_agg(g.name, ', ' ORDER BY g.name) AS genres, s.trailer, s.homepage 
        FROM shows s
        LEFT JOIN show_genres sg ON s.id = sg.show_id
        LEFT JOIN genres g ON sg.genre_id = g.id
        GROUP BY s.id
        LIMIT 15
        OFFSET ((%(page)s)-1)*15;
        """, {"page": page}
    )


def get_most_rated_shows(page, order_by='rating', order_direction='desc'):
    if order_by is None:
        order_by = 'rating'
    if order_direction is None:
        order_direction = 'desc'
    return data_manager.execute_select(f'''SELECT s.id, s.title, to_char(s.year, 'YYYY') AS year, s.runtime, 
        to_char(s.rating::float, '999.9') AS rating, string_agg(g.name, ', ' ORDER BY g.name) AS genres, s.trailer, s.homepage 
        FROM shows s
        LEFT JOIN show_genres sg ON s.id = sg.show_id
        LEFT JOIN genres g ON sg.genre_id = g.id
        GROUP BY s.id
        ORDER BY {order_by} {order_direction}
        LIMIT 15
        OFFSET ((%(page)s)-1)*15;
        ''', {"page": page}
    )


def get_genres_from_show(show_id):
    return data_manager.execute_select(
        f"""
        SELECT genres.name, show_id
        FROM show_genres
        JOIN genres ON genres.id = genre_id
        WHERE show_id = %(show_id)s;
        """, {"show_id": show_id}
    )


def get_show_count():
    return data_manager.execute_select(
        f"""
        SELECT COUNT(*) AS show_count 
        FROM shows;
        """
    )


def get_show_data(id):
    return data_manager.execute_select(
        f"""
        SELECT id, title, runtime, overview, trailer, rating
        FROM shows
        WHERE id = {id};
        """
    )


def get_all_id():
    return data_manager.execute_select(
        f'''
        SELECT id FROM shows;'''
    )


def get_show_actors(id):
    return data_manager.execute_select(
        f"""
        SELECT DISTINCT name
        FROM actors
        JOIN show_characters
        ON actors.id = show_characters.actor_id
        WHERE show_id = {id}
        LIMIT 3;
        """
    )


def get_seasons(id):
    return data_manager.execute_select(
        f"""
        SELECT season_number, title, overview
        FROM seasons
        WHERE {id} = show_id;
        """
    )


def get_100_actors():
    return data_manager.execute_select(
        f"""
        SELECT a.id, a.name, string_agg(s.title,', ' ORDER BY s.title) AS title, string_agg(sc.character_name,', ' ORDER BY sc.character_name) AS character_name, a.biography FROM actors a
        JOIN show_characters sc ON sc.actor_id=a.id
        JOIN shows s ON sc.show_id=s.id
        GROUP BY a.id
        ORDER BY a.birthday
        LIMIT 100;
        """
    )

def get_100_names():
    return data_manager.execute_select(
        f"""
        SELECT a.name FROM actors a
        ORDER BY a.birthday
        LIMIT 100;
        """
    )

