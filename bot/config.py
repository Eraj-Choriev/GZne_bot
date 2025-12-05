import os
from dataclasses import dataclass


@dataclass
class Config:
    bot_token: str
    admin_id: str | None = None
    admin_username: str | None = None

    @staticmethod
    def load() -> 'Config':
        return Config(
            bot_token=os.getenv('BOT_TOKEN', ''),
            admin_id=os.getenv('ADMIN_ID'),
            admin_username=os.getenv('ADMIN_USERNAME')
        )

