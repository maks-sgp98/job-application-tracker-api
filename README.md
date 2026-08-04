# Job Application Tracker API

Backend application for tracking job applications.

## Project goal

The application will help users save, organize and track their job applications.

## Planned technologies

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pytest
- Pydantic
- Docker

## Planned features

- User registration and authentication
- Create and manage job applications
- Track application statuses
- Search and filtering
- Application statistics
- REST API documentation

## Current status

The project is in active development.

## Development plan

The first version will include CRUD operations for job applications.

## Current functionality

- Add a job application
- Show all job applications
- Find an application by ID
- Update an application status
- Delete an application
- Search applications by company

## Installation

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Run tests

```bash
pytest -v
```

## Test coverage

```bash
pytest --cov=app.services --cov-report=term-missing
```

The service layer currently has 100% test coverage.

## Continuous integration

GitHub Actions automatically runs the test suite and checks service-layer coverage on pushes and pull requests.
