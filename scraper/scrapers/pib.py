import feedparser
from datetime import datetime

def scrape_pib():
    url = "https://www.divyabhaskar.co.in/rss-v1--category-1061.xml"
    
    articles = []
    
    try:
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:10]:
            articles.append({
                'headline': entry.title,
                'sourceURL': entry.link,
                'source': 'Divya Bhaskar',
                'language': 'gujarati',
                'location': {
                    'city': 'Ahmedabad',
                    'state': 'Gujarat'
                },
                'category': 'news',
                'scrapedAt': datetime.now()
            })
        
        print(f"Divya Bhaskar: Found {len(articles)} articles")
        return articles
    
    except Exception as e:
        print(f"Divya Bhaskar scraper error: {e}")
        return []