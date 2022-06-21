import asyncio
import itertools
import json
import os
import pathlib
import time
import traceback

import aiohttp
import discord
import mcstatus
from discord.ext import commands


class MinearchyBot(commands.Bot):
    session: aiohttp.ClientSession
    suggestions_channel: discord.TextChannel
    log_webhook: discord.Webhook
    up_ts: float

    embed_color = 0x3500FF

    def __init__(
        self, *, token: str, webhook_url: str, suggestions_channel_id: int
    ) -> None:
        ip = "play.landsofminearchy.com"
        self.mc_server = mcstatus.JavaServer.lookup(ip)
        self.mc_server.ip = ip
        self.mc_server.bedrock_ip = "bedrock.landsofminearchy.com"

        self.token = token
        self.webhook_url = webhook_url
        self.suggestions_channel_id = suggestions_channel_id
        super().__init__(
            command_prefix="=",
            owner_ids=set([512640455834337290]),
            intents=discord.Intents(
                guilds=True,
                members=True,
                messages=True,
                message_content=True,
            ),
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions.none(),
            max_messages=1000,
            strip_after_prefix=True,
            help_attrs=dict(
                brief="Sends help.",
                help="Sends all the commands of the bot, or help of a specific command and module.",
            ),
        )

    async def on_ready(self) -> None:
        self.up_ts = time.time()
        self.suggestions_channel = self.get_channel(self.suggestions_channel_id)
        print(f"\nConnected to Discord!\nUser: {self.user}\nID: {self.user.id}")
        await self.log_webhook.send("Bot is now online!")

    async def load_extensions(self) -> None:
        for fn in itertools.chain(
            map(
                lambda file_path: str(file_path).replace("/", ".")[:-3],
                pathlib.Path("./cogs").rglob("*.py"),
            ),
            ["jishaku"],
        ):
            try:
                await self.load_extension(fn)
                print(f"Loaded {fn}")
            except (commands.ExtensionFailed, commands.NoEntryPointError):
                print(f"Couldn't load {fn}:\n{traceback.format_exc()}")

    def run(self) -> None:
        async def runner() -> None:
            async with self, aiohttp.ClientSession() as session:
                self.session = session
                self.log_webhook = discord.Webhook.from_url(
                    self.webhook_url, session=self.session, bot_token=self.token
                )
                await self.load_extensions()
                await self.start(self.token, reconnect=True)

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            pass


with open("./config.json") as f:
    config = json.load(f)

for key in ["BOT_TOKEN", "WEBHOOK_URL"]:
    config.setdefault(key, os.getenv(key))

bot = MinearchyBot(
    token=config["BOT_TOKEN"],
    webhook_url=config["WEBHOOK_URL"],
    suggestions_channel_id=config["SUGGESTIONS_CHANNEL_ID"],
)

bot.run()
