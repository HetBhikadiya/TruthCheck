import pandas as pd
import nltk
import re
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Lowercase
    text = text.lower()
    # Tokenize
    tokens = text.split()
    # Remove stopwords + lemmatize
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return ' '.join(tokens)

def load_and_clean():
    # Load dataset
    df = pd.read_csv('data/fake_news.csv')
    print(f"Dataset loaded: {df.shape}")
    print(df.head())
    print(df['label'].value_counts())
    
    # Clean text
    df['clean_text'] = df['text'].apply(clean_text)
    df.to_csv('data/cleaned_news.csv', index=False)
    print("Cleaned data saved!")
    return df

if __name__ == '__main__':
    load_and_clean()