import json
import os
from datetime import datetime

# Local domain database file
DB_FILE = os.path.join(os.path.dirname(__file__), 'domains_db.json')

# Initial domain data
INITIAL_DOMAINS = {
    'ndtv.com': {'trustScore': 9, 'category': 'reliable', 'reportCount': 0},
    'thehindu.com': {'trustScore': 9, 'category': 'reliable', 'reportCount': 0},
    'bbc.com': {'trustScore': 10, 'category': 'reliable', 'reportCount': 0},
    'reuters.com': {'trustScore': 10, 'category': 'reliable', 'reportCount': 0},
    'pib.gov.in': {'trustScore': 10, 'category': 'reliable', 'reportCount': 0},
    'indianexpress.com': {'trustScore': 8, 'category': 'reliable', 'reportCount': 0},
    'timesofindia.com': {'trustScore': 8, 'category': 'reliable', 'reportCount': 0},
    'gujaratsamachar.com': {'trustScore': 7, 'category': 'reliable', 'reportCount': 0},
    'sandesh.com': {'trustScore': 7, 'category': 'reliable', 'reportCount': 0},
    'postcard.news': {'trustScore': 1, 'category': 'fake', 'reportCount': 50},
    'opindia.com': {'trustScore': 2, 'category': 'propaganda', 'reportCount': 30},
}

def load_db():
    if not os.path.exists(DB_FILE):
        save_db(INITIAL_DOMAINS)
        return INITIAL_DOMAINS
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def seed_initial_domains():
    db = load_db()
    for domain, data in INITIAL_DOMAINS.items():
        if domain not in db:
            db[domain] = data
            print(f"Added: {domain}")
        else:
            print(f"Already exists: {domain}")
    save_db(db)

def check_domain_in_db(domain):
    db = load_db()
    if domain in db:
        return {'found': True, **db[domain]}
    return {'found': False, 'trustScore': 5, 'category': 'unknown', 'reportCount': 0}

def flag_domain(domain, category='fake'):
    db = load_db()
    if domain in db:
        db[domain]['reportCount'] += 1
    else:
        db[domain] = {'trustScore': 2, 'category': category, 'reportCount': 1}
    save_db(db)
    print(f"Domain flagged: {domain}")

if __name__ == '__main__':
    print("Seeding initial domains...")
    seed_initial_domains()
    print("\nChecking ndtv.com:")
    print(check_domain_in_db('ndtv.com'))
    print("\nChecking postcard.news:")
    print(check_domain_in_db('postcard.news'))
    print("\nChecking unknown site:")
    print(check_domain_in_db('randomfakesite.com'))