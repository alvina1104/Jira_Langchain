from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = os.getenv('OPENROUTER_URL')
