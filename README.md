# Code-Against-Cancer

Web Based Application for Cancer Patients Who Need Nutritional Guidance

## Technologies

- Python
- Django
- Bootstrap
- YouTube API

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

## Testing

TODO: new information on testing coming soon.

## Team Members

- Edwin Peraza
- Daniel Ochoa
- Edward Cardenas
- Kalila Ingco
