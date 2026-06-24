import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGIN_START_HOUR = int(os.getenv("LOGIN_START_HOUR", 8))
    LOGIN_END_HOUR = int(os.getenv("LOGIN_END_HOUR", 18))

    DEV_LOGIN = os.getenv("DEV_LOGIN", "false").lower() == "true"