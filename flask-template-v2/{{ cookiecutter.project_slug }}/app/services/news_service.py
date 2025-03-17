from app.repositories.news_repo import inserir_news, obter_news


def lista_news():
    return obter_news()

def create_news(title, content):
    if not title or not content:
        return "Title and content are required fields.", 400

    try:
        inserir_news(title, content)
        return "News added successfully!"
    except Exception:
        return "An error occurred while adding the news."
