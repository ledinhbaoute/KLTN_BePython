from app import db
from sqlalchemy import text

def get_user_history_reading(user_id):
    query = text("""
                   SELECT hr.user_id, c.id as comic_id, cg.genre_id
        FROM history_reading hr
        JOIN chapters ch ON hr.chapter_id = ch.id
        JOIN comicbooks c ON ch.comicbook_id = c.id
        JOIN comicbooks_genres cg ON c.id = cg.comicbook_id
        WHERE hr.user_id = :user_id
        """)
    result = db.session.execute(query, {'user_id': user_id}).fetchall()
    history = [{'user_id': row.user_id, 'comic_id': row.comic_id, 'genre_id': row.genre_id} for row in result]
    return history

def get_all_genres():
    query = text("select * from genres;")
    result = db.session.execute(query).fetchall()
    genres = [row.id for row in result]
    return genres

def get_all_comic_genres():
    query = text("select * from comicbooks_genres")
    result = db.session.execute(query).fetchall()
    comic = [{'genre_id': row.genre_id, 'comicbook_id': row.comicbook_id} for row in result]
    return comic