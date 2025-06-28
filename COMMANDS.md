# Developer Commands

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
```

## Linting
```bash
pre-commit run --all-files
```

## Running Services
```bash
# API Server
uvicorn app:app --reload

# Celery Worker  
celery -A services.celery_app worker --loglevel=info --pool=solo

# Redis (if not running)
redis-server
```

## Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_endpoints.py
```

## Docker
```bash
# Build image
docker build -t aurelius-ai .

# Run container
docker run -p 8000:8000 --env-file .env aurelius-ai
```

## Linting
```bash
black .
isort .
flake8 .
```