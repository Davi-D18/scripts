from flask import Blueprint, jsonify
from app.services.news_service import get_all_news

news_bp = Blueprint('news', __name__)

@news_bp.route('/news', methods=['GET'])
def get_news():
    news = get_all_news()
    return jsonify([n.serialize() for n in news])
