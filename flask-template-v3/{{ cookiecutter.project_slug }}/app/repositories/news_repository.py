{% if cookiecutter.usar_banco_de_dados == "s" %}
from app.models.news import News
from app.extensions import db

def obter_news():
    return News.query.all()

def inserir_news(title, content):
    news = News(title=title, content=content)
    db.session.add(news)
    db.session.commit()
    return news
{% endif %}
