import os

from dotenv import load_dotenv

load_dotenv()

valid_password = os.getenv('valid_password')
valid_email = os.getenv('valid_email')
valid_login = os.getenv('valid_login')
valid_account = os.getenv('valid_account')
valid_phone = os.getenv('valid_phone')
invalid_phone = os.getenv('invalid_phone')
invalid_email = os.getenv('invalid_email')
invalid_password = os.getenv('invalid_password')
invalid_login = os.getenv('invalid_login')
invalid_account = os.getenv('invalid_account')