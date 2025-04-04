from app.repositories.news_repository import inserir_news, obter_news

def lista_news():
{% if cookiecutter.usar_serializacao == "n" %}
    news_list = obter_news()
    serialized_news = [
        {
            "id": new.id,
            'title': new.title,
            'content': new.content
        } for new
        in news_list
    ]
    return serialized_news
{% else %}
    return obter_news()
{% endif %}

def create_news(title, content):
    try:
        inserir_news(title, content)
        return "News adicionado!", 201
    except Exception:
        return "Erro ao adicionar News", 500
