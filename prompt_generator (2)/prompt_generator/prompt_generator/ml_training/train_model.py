#!/usr/bin/env python
"""
ml_training/train_model.py
==========================
Standalone script to train (or retrain) the PromptForge ML classifier.

Usage (from the project root):
    python ml_training/train_model.py

The script:
  1. Loads the sample dataset from generator/ml/dataset.py
  2. Trains a TF-IDF + Logistic Regression pipeline
  3. Evaluates on a held-out test split
  4. Saves the pipeline to generator/ml/saved_models/pipeline.pkl

Run this whenever you add new training data.
"""

import sys
import os

# Ensure the project root is on sys.path so we can import 'generator'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from generator.ml.train import train_model

if __name__ == '__main__':
    print("\n🔥  PromptForge – Model Training Script")
    print("=" * 50)
    train_model(verbose=True)
    print("\n✅  Model is ready. Start the server with:")
    print("    python manage.py runserver\n")
