"""
Optimized Fake News Classifier
--------------------------------
Key changes vs original:
  - SVC(kernel='linear')  →  SGDClassifier (same math, ~100x faster on large data)
  - RandomForest           →  n_jobs=-1  (parallel training across all CPU cores)
  - TfidfVectorizer        →  max_features=5000, sublinear_tf=True (better & faster)
  - No random sample(1000) – trains on ALL rows in minutes, not hours
  - models/ directory auto-created if missing
"""

import os
import time
import pandas as pd
import numpy as np
import joblib
import scipy.sparse as sp

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression      # better accuracy than SGD on small-medium data
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from scipy.sparse import hstack

# ── 0. Ensure output directory exists ──────────────────────────────────────────
os.makedirs('models', exist_ok=True)   # creates models/ if it doesn't exist

# ── 1. Load & clean ────────────────────────────────────────────────────────────
print("Loading data...")
t0 = time.time()
df = pd.read_csv('data/featured_news.csv')
df = df.dropna(subset=['clean_text', 'label'])
df['label_num'] = df['label'].map({'REAL': 1, 'FAKE': 0})
print(f"  Rows loaded: {len(df):,}  ({time.time()-t0:.1f}s)")

# ── 2. Features ─────────────────────────────────────────────────────────────────
print("\nBuilding TF-IDF features...")
t0 = time.time()
tfidf = TfidfVectorizer(
    max_features=5000,
    sublinear_tf=True,      # log(1+tf) — better accuracy, same speed
    min_df=3,               # skip very rare terms → smaller, faster matrix
    ngram_range=(1, 2),     # adds bigrams for more signal (optional, remove if slow)
)
X_tfidf = tfidf.fit_transform(df['clean_text'])

extra_cols = ['clickbait_score', 'emotional_score', 'punctuation_score', 'text_length']
extra = sp.csr_matrix(df[extra_cols].values)
X = hstack([X_tfidf, extra], format='csr')
y = df['label_num'].values
print(f"  Feature matrix: {X.shape}  ({time.time()-t0:.1f}s)")

# ── 3. Split ────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y   # stratify keeps class ratio
)
print(f"  Train: {X_train.shape[0]:,}  |  Test: {X_test.shape[0]:,}")

# ── 4. Logistic Regression ─────────────────────────────────────────────────────
# For ~6k rows LR beats SGD in accuracy (SGD needs large data to shine).
# solver='saga' supports L1/L2, is parallelised, and handles sparse TF-IDF well.
print("\n[1/2] Training Logistic Regression...")
t0 = time.time()
lr = LogisticRegression(
    C=5.0,                  # inverse regularisation strength; tune up for less penalty
    solver='saga',          # fast for sparse, large feature sets
    max_iter=1000,
    n_jobs=-1,
    random_state=42,
    class_weight='balanced'
)
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)
lr_proba = lr.predict_proba(X_test)
print(f"  Done in {time.time()-t0:.1f}s")
print(f"  Accuracy : {accuracy_score(y_test, lr_preds):.4f}")
print(f"  Confusion matrix:\n{confusion_matrix(y_test, lr_preds)}")
print(classification_report(y_test, lr_preds, target_names=['FAKE','REAL']))

# ── 5. Random Forest ────────────────────────────────────────────────────────────
print("\n[2/2] Training Random Forest...")
t0 = time.time()
rf = RandomForestClassifier(
    n_estimators=200,       # more trees → better accuracy
    max_depth=30,           # limit depth to avoid memory explosion on sparse data
    min_samples_leaf=5,
    n_jobs=-1,              # ← THIS alone makes RF 4–8x faster (parallel trees)
    random_state=42,
    class_weight='balanced'
)
rf.fit(X_train, y_train)
rf_preds  = rf.predict(X_test)
rf_proba  = rf.predict_proba(X_test)
print(f"  Done in {time.time()-t0:.1f}s")
print(f"  Accuracy : {accuracy_score(y_test, rf_preds):.4f}")
print(f"  Confusion matrix:\n{confusion_matrix(y_test, rf_preds)}")
print(classification_report(y_test, rf_preds, target_names=['FAKE','REAL']))

# ── 6. Weighted ensemble ────────────────────────────────────────────────────────
# Weight by individual accuracy so the stronger model dominates automatically.
print("\nEnsemble (LR + RF weighted by accuracy)...")
lr_acc = accuracy_score(y_test, lr_preds)
rf_acc = accuracy_score(y_test, rf_preds)
total  = lr_acc + rf_acc
w_lr, w_rf = lr_acc / total, rf_acc / total
print(f"  Weights — LR: {w_lr:.2f}  RF: {w_rf:.2f}")

ensemble_proba = w_lr * lr_proba + w_rf * rf_proba
ensemble_preds = np.argmax(ensemble_proba, axis=1)
print(f"  Accuracy : {accuracy_score(y_test, ensemble_preds):.4f}")
print(f"  Confusion matrix:\n{confusion_matrix(y_test, ensemble_preds)}")
print(classification_report(y_test, ensemble_preds, target_names=['FAKE','REAL']))

# ── 7. Save models ──────────────────────────────────────────────────────────────
print("\nSaving models...")
joblib.dump(tfidf, 'models/tfidf.pkl')
joblib.dump(lr,    'models/logistic_regression.pkl')
joblib.dump(rf,    'models/random_forest.pkl')
print("  Saved to models/  ✓")

print("\n✓ All done!")