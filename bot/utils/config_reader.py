from dataclasses import dataclass
from environs import Env
from pathlib import Path

BASE_DIR = Path(__file__).parent

env = Env()
env.read_env(f'{BASE_DIR}/.env')


@dataclass
class Config:
    token: str


def load_config():
    return Config(
        token=env("BOT_TOKEN"),
    )


config = load_config()