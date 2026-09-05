#!/bin/bash
# ─────────────────────────────────────────────────────
# Campus Impact — Quick Setup Script
# TAG SCT Changanyikeni Ministry Management System
# ─────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║       CAMPUS IMPACT — Setup Script               ║"
echo "║       TAG SCT Changanyikeni                      ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi
echo "✓ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate || source venv/Scripts/activate 2>/dev/null

# Install dependencies
echo "📥 Installing requirements..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Migrate
echo ""
echo "🗄️  Setting up database..."
python manage.py migrate --run-syncdb -v 0

# Seed data
echo "🌱 Seeding initial data..."
python manage.py seed_data

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  ✅ Setup Complete!                               ║"
echo "║                                                   ║"
echo "║  Run:  python manage.py runserver                 ║"
echo "║  Open: http://127.0.0.1:8000                      ║"
echo "║                                                   ║"
echo "║  Username: admin                                  ║"
echo "║  Password: campusimpact2024                       ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
