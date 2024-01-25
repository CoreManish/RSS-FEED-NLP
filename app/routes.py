# app/routes.py

from flask import render_template
from app import app
from app.services import update_articles
from app.models import Article

@app.route('/')
def index():
    update_articles()  # Fetch and update articles
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

