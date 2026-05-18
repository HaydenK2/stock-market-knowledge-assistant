import os
import getpass
from dotenv import load_dotenv


def _set_env(key: str):
    """ Internal helper - use to set env vars"""
    if key not in os.environ:
        os.environ[key] = getpass.getpass(f"{key}")


def set_env_variables():
    "call this to set up env variables"

    load_dotenv()  # Try .env first

    _set_env('USER_AGENT')
    _set_env('LANGCHAIN_TRACING_V2')
    _set_env('LANGCHAIN_ENDPOINT')
    _set_env('LANGCHAIN_API_KEY')
    _set_env('OPENAI_API_KEY')
    _set_env('TAVILY_API_KEY')


