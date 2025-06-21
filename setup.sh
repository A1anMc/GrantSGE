#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up Grant Application Dashboard..."

# Check for required tools
echo "📋 Checking prerequisites..."
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "pip3 is required but not installed. Aborting." >&2; exit 1; }

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

# Create .env file if it doesn't exist
echo "🔧 Setting up environment variables..."
if [ ! -f ../.env ]; then
    echo "Creating .env file..."
    cat > ../.env << EOL
# Application Environment
NODE_ENV=development
FLASK_ENV=development

# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# AI Service Configuration
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GROQ_API_KEY=your_groq_api_key

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/grant_dashboard

# Frontend Configuration
VITE_API_URL=http://localhost:5000
VITE_SUPABASE_URL=\${SUPABASE_URL}
VITE_SUPABASE_ANON_KEY=\${SUPABASE_ANON_KEY}
EOL
    echo "⚠️  Please update the .env file with your actual configuration values"
fi

# Build frontend
echo "🏗️  Building frontend..."
npm run build

cd ..

echo """
✅ Setup complete!

Next steps:
1. Update the .env file with your Supabase and AI service credentials
2. Run the database setup: python database/init.py
3. Start the development servers:
   - Backend: python app.py
   - Frontend: cd frontend && npm run dev
4. Run the initial grant scraper: python scrapers/grant_scraper.py

For more information, check the README.md and DEVELOPMENT.md files.
""" 