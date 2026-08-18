import os

from dotenv import load_dotenv

environment = os.getenv("APP_ENV", "development")
load_dotenv(f".env.{environment}")
