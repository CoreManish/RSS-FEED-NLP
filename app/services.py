# app/services.py

import feedparser
import spacy
from app import db
from app.models import Article

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


# http://rss.cnn.com/rss/cnn_topstories.rss
# http://qz.com/feed
# http://feeds.foxnews.com/foxnews/politics
# http://feeds.reuters.com/reuters/businessNews
# http://feeds.feedburner.com/NewshourWorld
# https://feeds.bbci.co.uk/news/world/asia/india/rss.xml

RSS_FEEDS = ['http://rss.cnn.com/rss/cnn_topstories.rss', 
             'http://qz.com/feed', 
             'http://feeds.foxnews.com/foxnews/politics', 
             'http://feeds.reuters.com/reuters/businessNews'
             'http://feeds.feedburner.com/NewshourWorld',
             'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml']

def categorize_text(text):
    doc = nlp(text)
    categories = []

    # Define keywords for each category
    terrorism_keywords = ['terrorism', 'protest', 'political unrest', 'riot']
    positive_keywords = ['positive', 'uplifting', 'joyful']
    natural_disaster_keywords = ['natural disaster', 'earthquake', 'flood', 'hurricane']

    # Check for relevant entities in the text
    for ent in doc.ents:
        if any(keyword in ent.text.lower() for keyword in terrorism_keywords):
            categories.append('Terrorism/Protest/Political Unrest/Riot')
        elif any(keyword in ent.text.lower() for keyword in positive_keywords):
            categories.append('Positive/Uplifting')
        elif any(keyword in ent.text.lower() for keyword in natural_disaster_keywords):
            categories.append('Natural Disasters')

    # If none of the predefined categories match, assign to 'Others'
    if not categories:
        categories.append('Others')

    return categories

def update_articles():
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            rss_category = entry.category if hasattr(entry, 'category') else 'Uncategorized'

            # Check if the article already exists
            existing_article = Article.query.filter_by(link=link).first()
            if existing_article is None:
                new_article = Article(title=title, link=link, rss_category=rss_category)

                # Categorize the article based on its content
                spacy_categories = categorize_text(entry.title)
                new_article.spacy_category = ', '.join(spacy_categories)

                db.session.add(new_article)

    db.session.commit()
