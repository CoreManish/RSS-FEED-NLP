# app/models.py

from app import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    rss_category = db.Column(db.String(50), nullable=False)
    spacy_category = db.Column(db.String(50))  # New column for spaCy-generated category
    link = db.Column(db.String(300), nullable=False, unique=True)
