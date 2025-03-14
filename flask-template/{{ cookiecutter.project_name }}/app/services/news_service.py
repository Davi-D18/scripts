from app.models.news import News
from app.extensions import db

def get_all_news():
    try:
        return News.query.all()
    except Exception:
        db.session.rollback()
        return []
