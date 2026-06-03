"""
train.py – Trains the intent/category classifier and saves it to disk.

Pipeline:
  TF-IDF vectoriser  →  Logistic Regression classifier

Run this file directly to (re-)train the model:
    python -m generator.ml.train
"""

import os
import pickle
import logging
from pathlib import Path

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.naive_bayes import MultinomialNB

# ---------------------------------------------------------------------------
# Local imports – support both direct execution and Django import
# ---------------------------------------------------------------------------
try:
    from generator.ml.dataset import TRAINING_DATA
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from generator.ml.dataset import TRAINING_DATA

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SAVED_MODELS_DIR = Path(__file__).resolve().parent / 'saved_models'
CLASSIFIER_PATH  = SAVED_MODELS_DIR / 'classifier.pkl'
VECTORIZER_PATH  = SAVED_MODELS_DIR / 'vectorizer.pkl'
PIPELINE_PATH    = SAVED_MODELS_DIR / 'pipeline.pkl'


def _ensure_dir() -> None:
    """Create saved_models directory if it does not exist."""
    SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)


def _build_dataset():
    """Return (texts, labels) lists from TRAINING_DATA."""
    texts  = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]
    return texts, labels


def train_model(verbose: bool = True) -> Pipeline:
    """
    Train a TF-IDF + Logistic Regression pipeline and persist it.

    Returns the fitted Pipeline object.
    """
    _ensure_dir()
    texts, labels = _build_dataset()

    # Split for evaluation (only during training; not stored)
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # ---------------------------------------------------------------------------
    # Pipeline: TF-IDF (char + word n-grams) → Logistic Regression
    # ---------------------------------------------------------------------------
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 2),       # unigrams + bigrams
            max_features=10_000,
            sublinear_tf=True,        # dampen term frequency
            strip_accents='unicode',
            lowercase=True,
            stop_words='english',
        )),
        ('clf', LogisticRegression(
            max_iter=1000,
            C=5.0,
            solver='lbfgs',
            random_state=42,
        )),
    ])

    pipeline.fit(X_train, y_train)

    # ---------------------------------------------------------------------------
    # Evaluate
    # ---------------------------------------------------------------------------
    if verbose:
        y_pred = pipeline.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"\n{'='*50}")
        print(f"  Model Training Complete")
        print(f"  Accuracy : {acc:.2%}")
        print(f"{'='*50}")
        print(classification_report(y_test, y_pred))

    # ---------------------------------------------------------------------------
    # Persist
    # ---------------------------------------------------------------------------
    with open(PIPELINE_PATH, 'wb') as f:
        pickle.dump(pipeline, f, protocol=pickle.HIGHEST_PROTOCOL)

    if verbose:
        print(f"  Pipeline saved → {PIPELINE_PATH}")

    return pipeline


def load_or_train() -> Pipeline:
    """
    Load an existing pipeline from disk, or train a fresh one.
    This is called at Django startup so the model is ready immediately.
    """
    if PIPELINE_PATH.exists():
        with open(PIPELINE_PATH, 'rb') as f:
            pipeline = pickle.load(f)
        logger.info("ML pipeline loaded from %s", PIPELINE_PATH)
        return pipeline

    logger.info("No saved pipeline found – training now …")
    return train_model(verbose=False)


# ---------------------------------------------------------------------------
# Allow direct execution: python -m generator.ml.train
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    train_model(verbose=True)
