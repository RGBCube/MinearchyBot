import discord
import time
import aiohttp
from discord.ext import commands
import os
import json
import asyncio
from mcstatus import MinecraftServer
import traceback
import pathlib


class MinearchyBot(commands.Bot):
    session: aiohttp.ClientSession
    log_webhook: discord.Webhook
    up_ts: float

    embed_color = 0x39FF14

    def __init__(self, token: str, webhook_url: str, /) -> None:
        ip = "play.landsofminearchy.com"
        self.mc_server = MinecraftServer.lookup(ip)
        self.mc_server.ip = ip
        self.mc_server.bedrock_ip = "bedrock.landsofminearchy.com"

        self.token = token
        self.webhook_url = webhook_url

        intents = discord.Intents(
            guilds=True,
            members=True,
            messages=True,
            message_content=True,
        )
        stuff_to_cache = discord.MemberCacheFlags.from_intents(intents)

        super().__init__(
            command_prefix="=",
            owner_ids={512640455834337290},
            intents=intents,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions.none(),
            member_cache_flags=stuff_to_cache,
            max_messages=1000,
            strip_after_prefix=True,
            help_attrs=dict(
                brief="Sends help.",
                help="Sends all the commands of the bot, or help of a specific command and module.",
            ),
        )     

    async def on_ready(self) -> None:
        self.up_ts = time.time()
        print(f"\nConnected to Discord!\nUser: {self.user}\nID: {self.user.id}")
        await self.log_webhook.send("Bot is now online!")

    async def load_extensions(self) -> None:
        for fn in map(
            lambda file_path: str(file_path).replace("/", ".")[:-3],
            pathlib.Path("./cogs").rglob("*.py"),
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

bot = MinearchyBot(config["BOT_TOKEN"], config["WEBHOOK_URL"])

if os.getenv("USING_REPLIT"):
    import webserver

    webserver.keep_alive()

bot.run()
