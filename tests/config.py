from functools import lru_cache
from app.config import Settings


@lru_cache
def get_testing_settings():
    return Settings(_env_file='../.env.test', _env_file_encoding='utf-8')
