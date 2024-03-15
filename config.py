from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('MAIL_HOST')
USERNAME = os.getenv('MAIL_USERNAME')
PASSWORD = os.getenv('MAIL_PASSWORD')
PORT = os.getenv('MAIL_PORT', 465)
