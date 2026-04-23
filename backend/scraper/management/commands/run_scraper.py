import time
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.core.management.base import BaseCommand
from pymongo import MongoClient

MONGO_URI = 'mongodb+srv://Truth_check_db_user:TruthCheck2025@cluster0.yfsilyr.mongodb.net/truthcheck?appName=Cluster0'

client = MongoClient(MONGO_URI)
db = client['truthcheck']
collection = db['localnews']

def scrape_gujarat_samachar():
    try:
        feed = feedparser.parse("https://www.gujaratsamachar.com/rss/top-stories")
        articles = []
        for entry in feed.entries[:10]:
            articles.append({
                'headline': entry.title,
                'sourceURL': entry.link,
                'source': 'Gujarat Samachar',
                'language': 'gujarati',
                'location': {'city': 'Ahmedabad', 'state': 'Gujarat'},
                'scrapedAt': datetime.now()
            })
        print(f"Gujarat Samachar: {len(articles)} articles")
        return articles
    except Exception as e:
        print(f"Gujarat Samachar error: {e}")
        return []

def scrape_ndtv():
    try:
        feed = feedparser.parse("https://feeds.feedburner.com/ndtvnews-india-news")
        articles = []
        for entry in feed.entries[:10]:
            articles.append({
                'headline': entry.title,
                'sourceURL': entry.link,
                'source': 'NDTV',
                'language': 'english',
                'location': {'city': 'National', 'state': 'India'},
                'scrapedAt': datetime.now()
            })
        print(f"NDTV: {len(articles)} articles")
        return articles
    except Exception as e:
        print(f"NDTV error: {e}")
        return []

def save_articles(articles):
    saved = 0
    for article in articles:
        existing = collection.find_one({'headline': article['headline']})
        if not existing:
            collection.insert_one(article)
            saved += 1
    print(f"Saved {saved} new articles")

class Command(BaseCommand):
    help = 'Run news scraper every 30 minutes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Auto scraper started! Runs every 30 minutes.')
        self.stdout.write('Press Ctrl+C to stop.')

        while True:
            print(f"\n{'='*40}")
            print(f"Scraping at {datetime.now()}")
            print(f"{'='*40}")

            all_articles = []
            all_articles.extend(scrape_gujarat_samachar())
            all_articles.extend(scrape_ndtv())

            print(f"Total scraped: {len(all_articles)}")
            save_articles(all_articles)

            print(f"Next run in 30 minutes...")
            time.sleep(1800)