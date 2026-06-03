#!/bin/bash
# setup.sh – One-command setup for PromptForge
# Usage: bash setup.sh

set -e

echo ""
echo "⚡  PromptForge – Setup Script"
echo "=================================="

# 1. Create virtual environment
echo ""
echo "→ Creating virtual environment…"
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "→ Installing dependencies…"
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 3. Train ML model
echo "→ Training ML model…"
python ml_training/train_model.py

# 4. Run Django migrations
echo "→ Running database migrations…"
python manage.py makemigrations generator
python manage.py migrate

# 5. Collect static files
echo "→ Collecting static files…"
python manage.py collectstatic --noinput -v 0

echo ""
echo "✅  Setup complete!"
echo ""
echo "Start the development server:"
echo "  source venv/bin/activate && python manage.py runserver"
echo ""
echo "Open in your browser: http://127.0.0.1:8000"
echo ""
