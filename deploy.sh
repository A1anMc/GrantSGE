#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting deployment process..."

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Git working directory is not clean. Please commit or stash changes first."
  exit 1
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

# Run tests
echo "🧪 Running tests..."
cd ..
python -m pytest

cd frontend
npm test
cd ..

# Build frontend
echo "🏗️ Building frontend..."
cd frontend
npm run build
cd ..

# Create database backup
echo "💾 Creating database backup..."
if [ -f "grants.db" ]; then
  cp grants.db "grants_backup_$(date +%Y%m%d_%H%M%S).db"
fi

# Run database migrations
echo "🔄 Running database migrations..."
flask db upgrade

echo "✅ Local deployment preparation complete!"
echo
echo "To deploy to Render.com:"
echo "1. Push your changes to GitHub"
echo "2. Go to your Render.com dashboard"
echo "3. Deploy the blueprint"
echo
echo "Your application will be available at:"
echo "- Frontend: https://grant-dashboard-frontend.onrender.com"
echo "- API: https://grant-dashboard-api.onrender.com" 