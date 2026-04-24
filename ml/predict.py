import joblib
import scipy.sparse as sp
import sys
import os
sys.path.append(os.path.dirname(__file__))

from features import clickbait_score, emotional_score, punctuation_score, text_length
from preprocess import clean_text

# Load models
tfidf = joblib.load('models/tfidf.pkl')
rf    = joblib.load('models/random_forest.pkl')

def predict(text):
    cleaned = clean_text(text)
    X_tfidf = tfidf.transform([cleaned])
    extra = sp.csr_matrix([[
        clickbait_score(text),
        emotional_score(text),
        punctuation_score(text),
        text_length(text)
    ]])
    from scipy.sparse import hstack
    X = hstack([X_tfidf, extra])
    
    proba = rf.predict_proba(X)[0]
    verdict = 'REAL' if proba[1] > 0.5 else 'FAKE'
    confidence = round(max(proba) * 100, 2)
    
    return {
        'verdict': verdict,
        'confidence': confidence,
        'fake_probability': round(proba[0] * 100, 2),
        'real_probability': round(proba[1] * 100, 2)
    }

if __name__ == '__main__':
    # Test with sample news
    fake_news = "SHOCKING: Obama secretly funding terrorist organizations exposed!"
    real_news = "The Federal Reserve raised interest rates by 0.25 percent on Wednesday"
    
    print("Testing fake news:")
    print(predict(fake_news))
    
    print("\nTesting real news:")
    print(predict(real_news))