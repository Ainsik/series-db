from data import data_manager


def get_shows():
    return data_manager.execute_select("""SELECT s.id, s.title, to_char(s.year, 'YYYY') AS year, s.runtime, to_char(s.rating::float, '999.9') AS rating, 
    string_agg(g.name, ', ' ORDER BY g.name) AS genres, s.trailer, s.homepage 
    FROM shows s
    JOIN show_genres sg ON s.id = sg.show_id
    JOIN genres g ON sg.genre_id = g.id
    GROUP BY s.id;""")


def get_most_rated_shows(page, order_by='rating', order_direction='desc'):
    if order_by is None:
        order_by = 'rating'
    if order_direction is None:
        order_direction = 'desc'
    return data_manager.execute_select(
        f'''
        SELECT id, title, year, runtime, rating, trailer, homepage 
        FROM shows
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
        SELECT title, runtime, overview, trailer, rating
        FROM shows
        WHERE id = {id};
        """
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
        SELECT id, name
        FROM actors
        LIMIT 100;
        """
    )
