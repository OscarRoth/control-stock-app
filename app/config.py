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

    # operador acceso temporal
    OPERADOR_TEMP_ACCESS = (
        os.getenv("OPERADOR_TEMP_ACCESS", "false").lower() == "true"
    )
    
    # Active Directory
    AD_SERVER = os.getenv("AD_SERVER")
    AD_DOMAIN = os.getenv("AD_DOMAIN")
    AD_BASE_DN = os.getenv("AD_BASE_DN")

    AD_GROUP_ADMIN = os.getenv("AD_GROUP_ADMIN")
    AD_GROUP_OPERADOR = os.getenv("AD_GROUP_OPERADOR")
    AD_GROUP_CONSULTA = os.getenv("AD_GROUP_CONSULTA")