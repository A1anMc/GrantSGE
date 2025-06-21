# Grant Application Dashboard

A comprehensive dashboard for managing grant applications, built with Flask, React, and Material-UI.

## Features

- User authentication and authorization
- Grant management and tracking
- AI-powered eligibility analysis
- Grant application draft generation
- Analytics and reporting
- Modern, responsive UI

## Tech Stack

### Backend
- Flask (Python web framework)
- SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- Redis (Caching and rate limiting)
- Anthropic Claude (AI integration)
- Prometheus (Monitoring)

### Frontend
- React with TypeScript
- Material-UI (Component library)
- React Query (Data fetching)
- Zustand (State management)
- Formik & Yup (Form handling)
- Vite (Build tool)

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/grant-application-dashboard.git
cd grant-application-dashboard
```

2. Set up the backend:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
flask db upgrade

# Run the development server
python app.py
```

3. Set up the frontend:
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Deployment on Render.com

1. Fork this repository to your GitHub account.

2. Create a new Render account at https://render.com if you haven't already.

3. Connect your GitHub account to Render.

4. Click "New +" and select "Blueprint" from the dropdown.

5. Select your forked repository.

6. Render will automatically detect the `render.yaml` configuration and create:
   - Backend API service
   - Frontend static site
   - Redis instance
   - PostgreSQL database

7. Configure the following environment variables in Render:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `SENTRY_DSN`: (Optional) Your Sentry DSN for error tracking

8. Deploy! Render will automatically:
   - Build and deploy the backend API
   - Build and deploy the frontend
   - Set up Redis and PostgreSQL
   - Configure the necessary environment variables

## API Documentation

API documentation is available at `/api/docs` when running the application. The documentation is generated using OpenAPI/Swagger.

## Testing

### Backend Tests
```bash
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 