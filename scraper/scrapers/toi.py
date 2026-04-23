import feedparser
from datetime import datetime

def scrape_toi():
    # Using Gujarat Samachar RSS instead (TOI blocks scrapers)
    url = "https://www.gujaratsamachar.com/rss/top-stories"
    
    articles = []
    
    try:
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:10]:
            articles.append({
                'headline': entry.title,
                'sourceURL': entry.link,
                'source': 'Gujarat Samachar',
                'language': 'gujarati',
                'location': {
                    'city': 'Ahmedabad',
                    'state': 'Gujarat'
                },
                'category': 'news',
                'scrapedAt': datetime.now()
            })
        
        print(f"Gujarat Samachar: Found {len(articles)} articles")
        return articles
    
    except Exception as e:
        print(f"Gujarat Samachar scraper error: {e}")
        return []