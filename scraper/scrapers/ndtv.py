import feedparser
from datetime import datetime

def scrape_ndtv():
    url = "https://feeds.feedburner.com/ndtvnews-india-news"
    
    articles = []
    
    try:
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:10]:
            articles.append({
                'headline': entry.title,
                'sourceURL': entry.link,
                'source': 'NDTV',
                'language': 'english',
                'location': {
                    'city': 'National',
                    'state': 'India'
                },
                'category': 'news',
                'scrapedAt': datetime.now()
            })
        
        print(f"NDTV: Found {len(articles)} articles")
        return articles
    
    except Exception as e:
        print(f"NDTV scraper error: {e}")
        return []