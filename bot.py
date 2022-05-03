import os
import pyrogram
from pyrogram import Client

if bool(os.environ.get("ENV", False)):
    from sample_config import Config
    from sample_config import LOGGER
else:
    from config import Config
    from config import LOGGER


class Bot(Client):
    # plugins = dict(
    #     root="ufs_bot"
    # )

    def __init__(self):
        super().__init__(
            "bot_session",
            api_hash=Config.API_HASH,
            api_id=Config.API_ID,
            bot_token=Config.TG_BOT_TOKEN,
            workers=Config.WORKERS,
            plugins={
                "root": "plugins"
            }
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.set_parse_mode("html")
        self.LOGGER(__name__).info(
            f"@{usr_bot_me.username}  started! "
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
