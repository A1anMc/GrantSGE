# Development Guide

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9+
- Node.js 18+
- Redis
- Git
- PostgreSQL (optional, SQLite for development)

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/grant-application-dashboard.git
cd grant-application-dashboard
```

2. Create and activate Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `FLASK_ENV`: development/production
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT token secret
- `DATABASE_URL`: Database connection string
- `ANTHROPIC_API_KEY`: Anthropic API key
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port
- `SENTRY_DSN`: Sentry DSN (optional)

5. Initialize the database:
```bash
flask db upgrade
```

6. Install frontend dependencies:
```bash
cd frontend
npm install
```

7. Start the development servers:

Backend:
```bash
# In the root directory
python app.py
```

Frontend:
```bash
# In the frontend directory
npm run dev
```

## Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Description of your changes"
```

3. Push your changes:
```bash
git push origin feature/your-feature-name
```

4. Create a pull request on GitHub

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

## Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=api --cov=models tests/

# Run specific test file
pytest tests/test_file.py
```

### Frontend Tests
```bash
# In the frontend directory
npm test

# Run with coverage
npm run coverage
```

## Database Migrations

Create a new migration:
```bash
flask db migrate -m "Description of changes"
```

Apply migrations:
```bash
flask db upgrade
```

Rollback migration:
```bash
flask db downgrade
```

## API Documentation

The API documentation is available at:
- Development: http://localhost:5000/api/docs
- Production: https://your-api-domain.com/api/docs

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

## Deployment

1. Prepare for deployment:
```bash
./deploy.sh
```

2. Push to GitHub:
```bash
git push origin main
```

3. Deploy on Render.com:
   - Connect GitHub repository
   - Configure environment variables
   - Deploy blueprint

## Performance Optimization

1. Backend:
   - Use caching appropriately
   - Optimize database queries
   - Profile API endpoints
   - Monitor memory usage

2. Frontend:
   - Lazy load components
   - Optimize bundle size
   - Use React.memo where appropriate
   - Implement virtual scrolling

## Security Best Practices

1. API Security:
   - Always validate input
   - Sanitize output
   - Use HTTPS
   - Implement rate limiting

2. Authentication:
   - Use secure password hashing
   - Implement token refresh
   - Set secure cookie options
   - Use proper CORS settings

3. Data Protection:
   - Validate file uploads
   - Sanitize user input
   - Implement proper access control
   - Regular security audits

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