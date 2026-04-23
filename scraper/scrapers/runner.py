import os
from pymongo import MongoClient
from datetime import datetime
from toi import scrape_toi
from pib import scrape_pib
from ndtv import scrape_ndtv

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://Truth_check_db_user:TruthCheck2025@cluster0.yfsilyr.mongodb.net/truthcheck?appName=Cluster0')

client = MongoClient(MONGO_URI)
db = client['truthcheck']
collection = db['localnews']

def save_articles(articles):
    saved = 0
    for article in articles:
        # Avoid duplicates — check if headline already exists
        existing = collection.find_one({'headline': article['headline']})
        if not existing:
            collection.insert_one(article)
            saved += 1
    print(f"Saved {saved} new articles to MongoDB")

def run_all_scrapers():
    print("=" * 40)
    print(f"Scraper started at {datetime.now()}")
    print("=" * 40)

    all_articles = []

    toi_articles = scrape_toi()
    all_articles.extend(toi_articles)

    pib_articles = scrape_pib()
    all_articles.extend(pib_articles)

    ndtv_articles = scrape_ndtv()
    all_articles.extend(ndtv_articles)

    print(f"\nTotal articles scraped: {len(all_articles)}")
    save_articles(all_articles)
    print("=" * 40)

if __name__ == '__main__':
    run_all_scrapers()