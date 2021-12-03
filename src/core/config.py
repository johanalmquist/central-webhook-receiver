import os


class Config(object):
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_DATABASE: str = os.getenv("DB_DATABASE", "")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")


config = Config
