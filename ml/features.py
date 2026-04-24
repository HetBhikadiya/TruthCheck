import re
import pandas as pd

# Clickbait phrases
CLICKBAIT_PHRASES = [
    'you won\'t believe', 'shocking', 'breaking', 'urgent',
    'exclusive', 'exposed', 'leaked', 'banned', 'secret',
    'doctors hate', 'this is why', 'what happened next'
]

# Emotional words
EMOTIONAL_WORDS = [
    'outrage', 'shocking', 'horrifying', 'disgusting', 'terrible',
    'amazing', 'incredible', 'unbelievable', 'disaster', 'crisis',
    'panic', 'fear', 'anger', 'hate', 'love', 'tragedy'
]

def clickbait_score(text):
    if not isinstance(text, str):
        return 0
    text_lower = text.lower()
    score = sum(1 for phrase in CLICKBAIT_PHRASES if phrase in text_lower)
    return score

def emotional_score(text):
    if not isinstance(text, str):
        return 0
    text_lower = text.lower()
    score = sum(1 for word in EMOTIONAL_WORDS if word in text_lower)
    return score

def punctuation_score(text):
    if not isinstance(text, str):
        return 0
    exclamations = text.count('!')
    caps_words = len(re.findall(r'\b[A-Z]{2,}\b', text))
    return exclamations + caps_words

def text_length(text):
    if not isinstance(text, str):
        return 0
    return len(text.split())

def extract_features(df):
    df['clickbait_score'] = df['title'].apply(clickbait_score)
    df['emotional_score'] = df['text'].apply(emotional_score)
    df['punctuation_score'] = df['text'].apply(punctuation_score)
    df['text_length'] = df['text'].apply(text_length)
    print("Features extracted!")
    print(df[['clickbait_score', 'emotional_score', 'punctuation_score', 'text_length']].describe())
    return df

if __name__ == '__main__':
    df = pd.read_csv('data/cleaned_news.csv')
    df = extract_features(df)
    df.to_csv('data/featured_news.csv', index=False)
    print("Feature file saved!")