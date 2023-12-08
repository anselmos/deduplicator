import os

from dotenv import load_dotenv

load_dotenv()

MAIN_PATH = os.getenv('MAIN_PATH')
DUPLICATES_PATH = os.getenv('DUPLICATES_PATH')