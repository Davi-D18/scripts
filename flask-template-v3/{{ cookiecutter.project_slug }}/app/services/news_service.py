from app.repositories.news_repository import inserir_news, obter_news


def lista_news():
    return obter_news()

def create_news(title, content):
    if not title or not content:
        return "Titulo e Content são obrigatórios", 400

    try:
        inserir_news(title, content)
        return "News adicionado!"
    except Exception:
        return "Erro ao adicionar News", 500
