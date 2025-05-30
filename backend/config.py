import os
from dotenv import load_dotenv

load_dotenv()

# Update DATABASE_URL to use PostgreSQL for production deployment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://myuser:mypassword@localhost/projectdb')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')