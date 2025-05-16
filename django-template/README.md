# LearningHub

LearningHub is a Django-based web application for online courses with user roles, course management, enrollment, and progress tracking.

## Features

- User registration and authentication with roles (student, teacher, admin)
- Course and lesson management
- Enrollment with student limits
- Course progress tracking
- Admin CRUD for all models
- Secure password storage and CSRF protection
- Testing with pytest and Django Test Client
- CI/CD with GitHub Actions and Railway deployment

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd django-template
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the app at `http://localhost:8000`

## Testing

Run tests with:

```bash
pytest
```

## Deployment

The project is configured for deployment on Railway with GitHub Actions CI/CD.

## Notes

- The default database is SQLite for development.
- Adjust settings for production as needed.
