# Code-Against-Cancer

Web Based Application for Cancer Patients Who Need Nutritional Guidance

## Technologies

- Python
- Django
- Bootstrap
- YouTube API
- Google Maps API
- SQLite
- JavaScript

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- **Python 3.8+**
- **Git**
- **Virtual Environment**
- **pip**

## Getting Started

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/DanOcho8/Code-Against-Cancer.git
```

### 2. Set Up a Virtual Environment

Create a virtual environment to isolate your project dependencies:

```bash
python3 -m venv venv
```

Activate the virtual environment:

- On Windows:

```bash
venv\Scripts\activate

```

- On macOS/Linux

```bash
source venv/bin/activate

```

### 3. Install Dependencies

Install the required dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

### 4. Navigate to the Project Directory

```bash
cd CodeAgainstCancer
```

### 5. Environmental Variables

Create a `.env` file in the project root and add the following environment variables:

```bash
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=[]
YOUTUBE_API_KEY=your_youtube_api_key
APP_ID=your_app_id
API_KEY=your_api_key
```

### 6. Apply Database Migrations

Apply the database migrations to set up the database schema:

```bash
python3 manage.py migrate
```

### 7. Run the Application

Run the Django development server:

```bash
python3 manage.py runserver
```

### 8.Testing

Run automated test cases:

```bash
python3 manage.py test
```

## Using Docker Container

### Prerequisite

Ensure Docker is installed on your local machine. You can download Docker from [Docker's official website](https://www.docker.com/products/docker-desktop).

### Running the Application with Docker

This application includes a `docker-compose.yml` file that allows you to run it using Docker for both development and production environments.

#### 1. Build Docker Images

First, ensure you’re in the root project directory, then build the Docker images:

#### 1. Run the Application in Development Mode

To run the application in development mode, use the development profile:

```bash
docker-compose --profile development up --build
```

This command:

- Starts the application with `python manage.py runserver`.
- Maps the project directory as a volume, enabling real-time updates as you code.

#### 2. Run the Application in Production Mode

For production, use the `production` profile:

```bash
docker-compose --profile production up --build
```

In production mode:

- The application runs with `gunicorn` for better performance.
- Volume mapping is disabled for a stable, consistent environment.

#### 5. Stopping the Docker Containers

To stop the running containers, use:

```bash
docker-compose down
```

This command stops and removes the containers, networks, and any temporary volumes.

### Notes

- If you make changes to dependencies, update your `requirements.txt` and rebuild the images with `docker-compose build`.
- Ensure your `.env` file is correctly configured with your environment variables before running Docker.

## Team Members

- Edwin Peraza
- Daniel Ochoa
- Edward Cardenas
- Kalila Ingco
- David Vu
