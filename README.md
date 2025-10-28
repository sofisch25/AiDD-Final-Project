# Campus Resource Hub

A centralized system for discovering and reserving shared campus resources (rooms, equipment, spaces) with AI-assisted features.

## Project Overview

**Course:** AiDD / X501 – AI-Driven Development  
**Instructor:** Prof. Jay Newquist  
**Team Repo:** [https://github.com/sofisch25/AiDD-Final-Project.git](https://github.com/sofisch25/AiDD-Final-Project.git)  
**Team Role:** Product Lead – PRD Owner  

## Features

- 🔍 **Centralized Resource Catalog** - Searchable database of campus resources
- 📅 **Automated Booking System** - Conflict detection and reservation management
- 👥 **Multi-User Support** - Students, Staff/Faculty, and Admin roles
- 🤖 **AI Resource Concierge** - Intelligent resource recommendations
- 💬 **Messaging System** - Threaded communication for approvals
- 📱 **Responsive Web Interface** - Mobile-friendly design

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (development) / PostgreSQL (production)
- **Frontend:** HTML, CSS, JavaScript
- **AI Integration:** OpenAI API / Local LLM
- **Authentication:** Flask-Login with email/password

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sofisch25/AiDD-Final-Project.git
   cd AiDD-Final-Project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   # Add your OpenAI API key and other settings
   ```

6. **Initialize the database**
   ```bash
   python init_db.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   
   Open your browser and navigate to: `http://localhost:5000`

## Database Setup

### Initial Migration

The application uses SQLite for development. Database initialization is handled automatically:

```bash
# Initialize database with sample data
python init_db.py

# Or run migrations manually
python migrate.py
```

### Database Schema

Key tables:
- `users` - User accounts and roles
- `resources` - Campus resources (rooms, equipment)
- `bookings` - Reservation records
- `messages` - Communication threads
- `reviews` - Resource ratings and feedback

### Sample Data

The initialization script creates:
- 3 user accounts (student, staff, admin)
- 10+ sample resources
- Sample booking history

## Development

### Project Structure

```
AiDD-Final-Project/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization
├── migrate.py            # Database migrations
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── docs/                # Documentation
│   ├── wireframes/      # UI wireframes
│   └── api/            # API documentation
├── static/              # CSS, JS, images
├── templates/           # HTML templates
└── models/              # Database models
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app

# Run specific test file
python -m pytest tests/test_auth.py
```

### Code Style

This project follows PEP 8 style guidelines:

```bash
# Check code style
flake8 app.py

# Auto-format code
black app.py
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///campus_hub.db

# OpenAI API (for AI features)
OPENAI_API_KEY=your-openai-api-key

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## API Documentation

### Authentication Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Resource Endpoints

- `GET /api/resources` - List all resources
- `GET /api/resources/<id>` - Get specific resource
- `POST /api/resources` - Create new resource (admin)
- `PUT /api/resources/<id>` - Update resource (admin)
- `DELETE /api/resources/<id>` - Delete resource (admin)

### Booking Endpoints

- `GET /api/bookings` - List user bookings
- `POST /api/bookings` - Create new booking
- `PUT /api/bookings/<id>` - Update booking
- `DELETE /api/bookings/<id>` - Cancel booking

## Deployment

### Production Setup

1. **Use PostgreSQL instead of SQLite**
2. **Set environment variables**
3. **Use a production WSGI server (Gunicorn)**
4. **Set up reverse proxy (Nginx)**

### Docker Deployment

```bash
# Build Docker image
docker build -t campus-resource-hub .

# Run container
docker run -p 5000:5000 campus-resource-hub
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**Database connection errors:**
- Ensure SQLite file permissions are correct
- Check DATABASE_URL in .env file

**Import errors:**
- Verify virtual environment is activated
- Run `pip install -r requirements.txt`

**Port already in use:**
- Change port in app.py or kill existing process
- Use `lsof -i :5000` to find process using port 5000

### Getting Help

- Check the [Issues](https://github.com/sofisch25/AiDD-Final-Project/issues) page
- Review the [PRD](Campus_Resource_Hub_PRD.md) for project requirements
- Contact the development team

## License

This project is part of the AiDD/X501 course at [University Name]. All rights reserved.

## Team

- **Product Lead:** [Your Name]
- **Development Team:** [Team Members]
- **Course:** AiDD/X501 - AI-Driven Development
- **Instructor:** Prof. Jay Newquist
