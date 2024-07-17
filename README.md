Install bootstrap 
- pip install django-bootstrap-v5


# GenZ Project

This project is a Django application with Celery for background task processing and Redis as the message broker.

## Requirements

- Python 3.9
- Django 4.2.13
- Celery 5.4.0
- Redis
- Other dependencies as listed in `Requirements.txt`

## Installation

### macOS

1. **Install Homebrew:**
    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. **Install Redis:**
    ```sh
    brew install redis
    brew services start redis
    ```

3. **Clone the repository and navigate to the project directory:**
    ```sh
    git clone <repository-url>
    cd <project-directory>
    ```

4. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

5. **Install Python dependencies:**
    ```sh
    pip install -r Requirements.txt
    ```

6. **Run database migrations:**
    ```sh
    python manage.py migrate
    ```

7. **Start the Django development server:**
    ```sh
    python manage.py runserver
    ```

8. **Start Celery worker:**
    ```sh
    celery -A GenZ worker -l info
    ```

### Linux

1. **Install Redis:**
    ```sh
    sudo apt update
    sudo apt install redis-server
    sudo systemctl enable redis-server.service
    sudo systemctl start redis-server.service
    ```

2. **Clone the repository and navigate to the project directory:**
    ```sh
    git clone <repository-url>
    cd <project-directory>
    ```

3. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4. **Install Python dependencies:**
    ```sh
    pip install -r Requirements.txt
    ```

5. **Run database migrations:**
    ```sh
    python manage.py migrate
    ```

6. **Start the Django development server:**
    ```sh
    python manage.py runserver
    ```

7. **Start Celery worker:**
    ```sh
    celery -A GenZ worker -l info
    ```

### Windows

1. **Install Redis:**
    - Download Redis from https://github.com/microsoftarchive/redis/releases
    - Extract the zip file and run `redis-server.exe`.

2. **Clone the repository and navigate to the project directory:**
    ```sh
    git clone <repository-url>
    cd <project-directory>
    ```

3. **Create and activate a virtual environment:**
    ```sh
    python -m venv .venv
    .venv\Scripts\activate
    ```

4. **Install Python dependencies:**
    ```sh
    pip install -r Requirements.txt
    ```

5. **Run database migrations:**
    ```sh
    python manage.py migrate
    ```

6. **Start the Django development server:**
    ```sh
    python manage.py runserver
    ```

7. **Start Celery worker:**
    ```sh
    celery -A GenZ worker -l info
    ```

## Configuration

Ensure the following settings are present in your `settings.py`:

```python
# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
