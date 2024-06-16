from dataclasses import dataclass
from environs import Env
from pathlib import Path

BASE_DIR = Path(__file__).parent

env = Env()
env.read_env(f'{BASE_DIR}/.env')


@dataclass
class Config:
    token: str
    # super_users: list[int]
    # postgres_pass: str
    # postgres_user: str
    # postgres_host: str
    # postgres_db: str


def load_config():
    return Config(
        token=env("BOT_TOKEN"),
        # super_users=[int(_id) for _id in env('SUPERUSERS_TELEGRAM_ID').split() if _id.isdigit()],
        # postgres_db=env("POSTGRES_DB"),
        # postgres_host=env("POSTGRES_HOST"),
        # postgres_user=env("POSTGRES_USER"),
        # postgres_pass=env("POSTGRES_PASSWORD"),
    )


config = load_config()