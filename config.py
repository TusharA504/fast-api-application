import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


class Settings:
    TITLE = "Learning FastApi"
    VERSION = "0.1.0"
    DESCRIPTION = """
    Hi I am Learning FastApi"""
    NAME = "Tushar Ahire"
    EMAIL = "dummy@gmail.com"
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE")
    MYSQl_DATABASE_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_USER_PASSWORD}@{DB_HOST}/fast_api'
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"


setting = Settings()
