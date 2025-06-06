import os 
from dotenv import load_dotenv, find_dotenv 

def load_env():
    load_dotenv(find_dotenv())

def get_nvidia_api_key():
    load_env()
    return os.getenv("NVIDIA_API_KEY")

def get_groq_api_key():
    load_env()
    return os.getenv("GROQ_API_KEY")
