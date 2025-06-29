# Development Guide

## 🛠️ Setup

### Prerequisites

- Python 3.11+
- Node.js 20.11+
- SQLite

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/grant-dashboard.git
cd grant-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
cd frontend && npm install
```

### Environment Variables

Create a `.env` file in the root directory with:

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_key

# Database Configuration
DATABASE_URL=sqlite:///grants.db

# CORS Configuration
CORS_ORIGINS=http://localhost:5173

# Monitoring Configuration
SENTRY_DSN=your_sentry_dsn
```

## 🏗️ Project Structure

```
grant-dashboard/
├── api/                 # Backend API
│   ├── routes/         # API endpoints
│   ├── models/         # Database models
│   └── utils/          # Helper functions
├── frontend/           # React frontend
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   └── services/   # API services
├── tests/              # Test suite
└── docs/               # Documentation
```

## 🚀 Development Workflow

### Running Locally

1. Start the backend:
```bash
python app.py
```

2. Start the frontend:
```bash
cd frontend
npm run dev
```

### Database Management

Initialize the database:
```bash
flask db upgrade
```

Create a new migration:
```bash
flask db migrate -m "Description"
```

### Testing

Run backend tests:
```bash
pytest

# With coverage
pytest --cov=api
```

Run frontend tests:
```bash
cd frontend
npm test
```

## 📚 API Documentation

The API documentation is available at:
- Local: http://localhost:5000/api/docs
- Production: https://your-api-domain.com/api/docs

## 🔄 Git Workflow

1. Create a feature branch:
```bash
git checkout -b feature/your-feature
```

2. Make your changes and commit:
```bash
git add .
git commit -m "feat: add new feature"
```

3. Push changes:
```bash
git push origin feature/your-feature
```

4. Create a pull request to main

## 📦 Deployment

The application is deployed on Render.com:

1. Backend API (Python/Flask):
   - Automatic deployments from main
   - Uses Gunicorn server
   - SQLite database

2. Frontend (React):
   - Static site hosting
   - Automatic deployments from main
   - Built with Vite

### Environment Variables (Production)

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_key

# Database Configuration
DATABASE_URL=sqlite:///grants.db

# CORS Configuration
CORS_ORIGINS=https://your-frontend-domain.com

# Monitoring
SENTRY_DSN=your_sentry_dsn

# Optional: Email Configuration
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USERNAME=your_username
EMAIL_PASSWORD=your_password
EMAIL_FROM=noreply@yourdomain.com
```

### Required Production Settings

The following must be configured in production:

- Secret key for Flask
- JWT secret key
- CORS origins
- Sentry DSN (optional but recommended)
- Email configuration: Required if you want to send email notifications

## 📊 Monitoring

The application includes:

1. Prometheus metrics:
   - Request latency
   - Error rates
   - System metrics

2. Grafana dashboards:
   - API performance
   - System resources
   - User activity

3. Sentry error tracking:
   - Exception monitoring
   - Performance tracking
   - User feedback

## 🔒 Security

1. Authentication:
   - JWT tokens
   - Refresh token rotation
   - Password hashing with bcrypt

2. Authorization:
   - Role-based access control
   - Resource ownership checks
   - API scope validation

3. API Security:
   - Rate limiting
   - CORS protection
   - Input validation
   - SQL injection prevention

## Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes
- Maximum line length: 100 characters

### TypeScript/React
- Follow ESLint configuration
- Use functional components
- Use TypeScript types/interfaces
- Document complex components
- Use Material-UI components

## Debugging

### Backend
- Use Flask debug mode
- Check logs in `logs/` directory
- Use Python debugger (pdb)
- Monitor Redis with redis-cli

### Frontend
- Use React Developer Tools
- Check browser console
- Use debugger statement
- Monitor network requests

## Common Issues

1. Database connection issues:
   - Check DATABASE_URL in .env
   - Ensure database server is running
   - Verify database exists

2. Redis connection issues:
   - Check Redis server is running
   - Verify REDIS_HOST and REDIS_PORT
   - Check Redis connection in logs

3. Frontend build issues:
   - Clear node_modules and reinstall
   - Check for TypeScript errors
   - Verify environment variables

4. Authentication issues:
   - Check JWT_SECRET_KEY
   - Verify token expiration
   - Check Redis for blacklisted tokens

## Contributing

1. Review the BLUEPRINT.md file
2. Follow the development workflow
3. Write tests for new features
4. Update documentation
5. Submit pull requests

## Support

- Create GitHub issues for bugs
- Use pull requests for features
- Check documentation first
- Join team discussions

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
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
VITE_SUPABASE_URL=${SUPABASE_URL}
VITE_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}

# Security
JWT_SECRET_KEY=your_jwt_secret_key
CORS_ORIGINS=http://localhost:3000,http://localhost:5000

# Monitoring & Logging
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=debug

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Scraper Configuration
GRANT_CONNECT_API_KEY=your_grant_connect_api_key
SCRAPER_INTERVAL=86400  # 24 hours in seconds

# Optional: Email Configuration
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_smtp_username
SMTP_PASSWORD=your_smtp_password
EMAIL_FROM=noreply@yourdomain.com

# Optional: Storage Configuration
STORAGE_PROVIDER=supabase  # or 's3' if using AWS S3
S3_BUCKET_NAME=your_bucket_name
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
```

### Required Variables
- `SUPABASE_URL` and `SUPABASE_ANON_KEY`: Get these from your Supabase project settings
- `DATABASE_URL`: Your PostgreSQL connection string
- At least one AI service key (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GROQ_API_KEY`)
- `JWT_SECRET_KEY`: A secure random string for JWT token signing

### Optional Variables
- `SENTRY_DSN`: For error tracking (recommended for production)
- Email configuration: Required if you want to send email notifications
- Storage configuration: Required if you want to use S3 instead of Supabase Storage 