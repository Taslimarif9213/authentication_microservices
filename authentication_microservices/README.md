# authentication_microservice

## Getting Started

Follow these steps to run the project on your local machine:

### Prerequisites

1. Python: Make sure you have Python installed on your machine. If not, you can download it from [Python's official website](https://www.python.org/downloads/).

### Setting Up a Virtual Environment

1. Create a virtual environment (venv) in the project directory:
    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

### Database Configuration

1. Update the database configuration in `core/settings/base.py` based on your MySQL configuration:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'your_db_host',    # Typically 'localhost'
            'PORT': 'your_db_port',    # Typically '3306'
        }
    }
    ```

### Apply Migrations

1. Apply initial migrations to set up the database schema:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Run the Development Server

1. Start the development server:
    ```bash
    python manage.py runserver
    ```

2. Open a web browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the project.
