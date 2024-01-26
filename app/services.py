# app/services.py

# import from other files
from app import db
from app.models import Article

# import library
from app.nltk_model import categorize
from app.spacy_model import categorize_text
import feedparser


RSS_FEEDS = ['http://rss.cnn.com/rss/cnn_topstories.rss', 
             'http://qz.com/feed', 
             'http://feeds.foxnews.com/foxnews/politics', 
             'http://feeds.reuters.com/reuters/businessNews'
             'http://feeds.feedburner.com/NewshourWorld',
             'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml']

def update_articles():
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            rss_category = entry.category if hasattr(entry, 'category') else 'Uncategorized'
            nltk_category = categorize(entry.title)

            # Check if the article already exists
            existing_article = Article.query.filter_by(link=link).first()
            if existing_article is None:
                new_article = Article(title=title, link=link, rss_category=rss_category, nltk_category=nltk_category)

                # Categorize the article based on its content
                spacy_categories = categorize_text(entry.title)
                new_article.spacy_category = ', '.join(spacy_categories)

                db.session.add(new_article)

    db.session.commit()
