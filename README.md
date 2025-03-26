# Grocer Ease Landing Page

A modern landing page for Grocer Ease, featuring a responsive design, interactive features, and admin dashboard.

## Features

- Modern, responsive design
- Interactive feature slider
- Email subscription system
- Interest tracking
- Contact form
- Admin dashboard with statistics
- MongoDB integration for data storage

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
MONGO_URI=your_mongodb_uri
```

4. Run the application:
```bash
python app.py
```

The application will be available at http://127.0.0.1:5000
