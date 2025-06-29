# Grant Application Dashboard

An intelligent grant management co-pilot that helps non-profits find and win funding.

## 🎯 Project Goal

This isn't just a database of grants - it's an active workflow tool that automates the most painful parts of the grant-seeking process:

- **Discovery**: Sifting through hundreds of irrelevant opportunities
- **Vetting**: Reading dozens of pages of guidelines just to see if you're eligible
- **Management**: Juggling deadlines, tasks, and documents across multiple applications
- **Writing**: Answering the same repetitive questions over and over again

## 🚀 Features

- Automated grant discovery and scraping
- AI-powered eligibility analysis
- Smart application drafting assistance
- Document management and organization
- Deadline tracking and reminders
- Team collaboration tools

## 🛠️ Tech Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python + Flask
- **Database**: SQLite (with migration support)
- **AI**: OpenAI/Anthropic/Groq
- **Deployment**: Render.com

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- Git

## 🏁 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/grant-application-dashboard.git
cd grant-application-dashboard
```

2. Run the setup script:
```bash
./setup.sh
```

3. Update the `.env` file with your credentials:
```bash
# Required environment variables
OPENAI_API_KEY=your_openai_key  # or use ANTHROPIC_API_KEY/GROQ_API_KEY
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
```

4. Start the development servers:

Backend:
```bash
# In the root directory
python app.py
```

Frontend:
```bash
# In the frontend directory
cd frontend
npm run dev
```

## 🚀 Deployment

The application is configured for deployment on Render.com with the following services:

1. Backend API (grant-dashboard-api):
   - Python/Flask application
   - SQLite database
   - Automatic deployments from main branch

2. Frontend (grant-dashboard-frontend):
   - Static site hosting
   - Built with Vite
   - Automatic deployments from main branch

Configuration is managed through `render.yaml` in the root directory.

## 📚 Documentation

- [Project Blueprint](BLUEPRINT.md)
- [Development Guide](DEVELOPMENT.md)
- [API Documentation](http://localhost:5000/api/docs) (when running locally)

## 🧪 Testing

Run backend tests:
```bash
pytest
```

Run frontend tests:
```bash
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/)/[Anthropic](https://anthropic.com/)/[Groq](https://groq.com/) for AI capabilities
- [Render](https://render.com/) for hosting 