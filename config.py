import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://grocerEase:pinakisir123@grocerease1.tzatn.mongodb.net/grocer_ease_db?retryWrites=true&w=majority')
DB_NAME = os.getenv('DB_NAME', 'grocer_ease_db')

# Admin Configuration
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'please')

# Contact Information
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'abc@gmail.com')

# Application Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here') 