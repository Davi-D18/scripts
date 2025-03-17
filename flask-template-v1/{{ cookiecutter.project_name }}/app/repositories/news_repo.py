from app.extensions import db
from app.models.news import News

class NewsRepository:
    @staticmethod
    def get_all():
        return News.query.all()
    
    @staticmethod
    def create(news_data):
        news = News(**news_data)
        db.session.add(news)
        db.session.commit()
        return news
