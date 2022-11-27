from __future__ import annotations

__all__ = ("MinearchyBot",)

from asyncio import run as run_coro
from inspect import cleandoc as strip_doc
from itertools import chain as chain_iter
from pathlib import Path
from time import time as current_time
from traceback import format_exc as format_exit

from aiohttp import ClientSession as AIOHTTPSession
from discord import AllowedMentions, Game, Intents, Webhook
from discord.ext.commands import (
    Bot as CommandsBot,
    ExtensionFailed,
    NoEntryPointError,
    when_mentioned_or,
)

from .minecraft_server import GeyserServer
from .util import override


class MinearchyBot(CommandsBot):
    ready_timestamp: float
    log_webhook: Webhook

    def __init__(self, *, token: str, webhook_url: str) -> None:
        self.token = token
        self.webhook_url = webhook_url

        self.server = GeyserServer(
            java_ip="play.landsofminearchy.com",
            bedrock_ip="bedrock.landsofminearchy.com",
        )

        super().__init__(
            command_prefix=when_mentioned_or("="),
            strip_after_prefix=True,
            case_insensitive=True,
            status=Game("on play.landsofminearchy.com"),
            owner_ids={512640455834337290, 160087716757897216},
            allowed_mentions=AllowedMentions.none(),
            max_messages=100,
            intents=Intents(
                guilds=True,
                members=True,
                messages=True,
                message_content=True,
            ),
            help_attrs=dict(
                brief="Sends help.",
                help="Sends all the commands of the bot, or help of a specific command or module.",
            ),
        )

    @override
    async def on_ready(self) -> None:
        print(
            strip_doc(
                f"""
                Connected to Discord!
                User: {self.user}
                ID: {self.user.id}
                """
            )
        )

        self.ready_timestamp = current_time()
        await self.log_webhook.send("Bot is now online!")

    async def load_extensions(self) -> None:
        cogs = Path(__file__).parent / "cogs"
        for file_name in chain_iter(
            map(
                lambda file_path: ".".join(file_path.relative_to(cogs.parent.parent).parts)[:-3],
                cogs.rglob("*.py"),
            ),
            ("jishaku",),
        ):
            try:
                await self.load_extension(file_name)
                print(f"Loaded {file_name}")
            except (ExtensionFailed, NoEntryPointError):
                print(f"Couldn't load {file_name}:\n{format_exit()}")

    @override
    def run(self) -> None:
        async def runner() -> None:
            async with self, AIOHTTPSession() as self.session:
                self.log_webhook = Webhook.from_url(
                    self.webhook_url, session=self.session, bot_token=self.token
                )
                await self.load_extensions()
                await self.start(self.token, reconnect=True)

        try:
            run_coro(runner())
        except KeyboardInterrupt:
            pass
