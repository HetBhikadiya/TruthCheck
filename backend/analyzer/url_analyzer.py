import requests
import whois
from datetime import datetime
from urllib.parse import urlparse

# Trusted domains list
TRUSTED_DOMAINS = [
    'bbc.com', 'reuters.com', 'ndtv.com', 'thehindu.com',
    'indianexpress.com', 'timesofindia.com', 'pib.gov.in',
    'hindustantimes.com', 'scroll.in', 'thewire.in'
]

# Blacklisted domains
BLACKLISTED_DOMAINS = [
    'postcard.news', 'opindia.com', 'swarajyamag.com',
    'thecognate.com', 'newsmobile.in'
]

def extract_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        return domain
    except:
        return None

def check_ssl(url):
    return url.startswith('https://')

def check_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age_days = (datetime.now() - creation_date).days
            return age_days
        return None
    except:
        return None

def check_trust_status(domain):
    if domain in TRUSTED_DOMAINS:
        return 'trusted'
    elif domain in BLACKLISTED_DOMAINS:
        return 'blacklisted'
    return 'unknown'

def analyze_url(url):
    result = {
        'url': url,
        'domain': None,
        'ssl': False,
        'domain_age_days': None,
        'trust_status': 'unknown',
        'trust_score': 50,
        'verdict': 'UNVERIFIED'
    }

    domain = extract_domain(url)
    if not domain:
        return result

    result['domain'] = domain
    result['ssl'] = check_ssl(url)
    result['domain_age_days'] = check_domain_age(domain)
    result['trust_status'] = check_trust_status(domain)

    # Calculate trust score
    score = 50
    if result['ssl']:
        score += 10
    if result['domain_age_days']:
        if result['domain_age_days'] > 365 * 5:
            score += 20
        elif result['domain_age_days'] > 365:
            score += 10
        elif result['domain_age_days'] < 180:
            score -= 20
    if result['trust_status'] == 'trusted':
        score += 30
    elif result['trust_status'] == 'blacklisted':
        score -= 40

    result['trust_score'] = max(0, min(100, score))

    if result['trust_score'] >= 70:
        result['verdict'] = 'LIKELY REAL'
    elif result['trust_score'] >= 40:
        result['verdict'] = 'UNVERIFIED'
    else:
        result['verdict'] = 'LIKELY FAKE'

    return result

if __name__ == '__main__':
    # Test it
    test_urls = [
        'https://www.ndtv.com/india-news/test',
        'https://www.bbc.com/news/test',
        'http://postcard.news/fake-story'
    ]
    for url in test_urls:
        print(analyze_url(url))
        print()