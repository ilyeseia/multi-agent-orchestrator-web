#!/bin/bash

echo "🚀 Multi-Agent Orchestrator - Installation"

# Check Python version
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Initialize database
flask db init || true
flask db migrate || true
flask db upgrade || true

# Create admin user
flask create-admin

echo "✅ Installation complete!"
echo "🚀 Run: python app.py"
