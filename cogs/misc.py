from __future__ import annotations

from typing import TYPE_CHECKING
from discord.ext import commands
import datetime
from collections import defaultdict, deque
import discord
from discord.utils import escape_markdown as es_md
import platform

import time

if TYPE_CHECKING:
    from bot import MinearchyBot


class Miscellanious(
    commands.Cog,
    name="Miscellanious",
    description="Various utilities.",
):
    def __init__(self, bot: MinearchyBot, /) -> None:
        self.bot = bot
        self.bot.help_command.cog = self
        self.sniped = defaultdict(deque)

    def cog_unload(self) -> None:
        self.bot.help_command.cog = None
        self.bot.help_command.hidden = True

    @commands.command(brief="Sends the bots ping.", help="Sends the bots ping.")
    async def ping(self, ctx: commands.Context, /) -> None:
        ts = time.time()
        message = await ctx.reply("Pong!")
        ts = time.time() - ts
        await message.edit(content=f"Pong! `{int(ts * 1000)}ms`")

    @commands.command(
        brief="Sends info about the bot.", help="Sends info about the bot."
    )
    async def info(self, ctx: commands.Context, /) -> None:
        embed = discord.Embed(title="Bot Info", color=self.bot.embed_color)
        embed.add_field(
            name="Python Version", value=f"```v{platform.python_version()}```"
        )
        embed.add_field(
            name="Uptime",
            value=f"```{datetime.timedelta(seconds=int(time.time() - self.bot.up_ts))}```",
        )
        await ctx.reply(embed=embed)

    @commands.command(brief="Hello!", help="Hello!")
    async def hello(self, ctx: commands.Context, /) -> None:
        await ctx.reply(f"Hi {es_md(ctx.author.name)}, yes the bot is running :)")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message, /) -> None:
        if not message.guild:
            return

        logs = self.sniped[message.channel.id]

        logs.appendleft((message, int(time.time())))

        while len(logs) > 5:
            logs.pop()

    @commands.command(
        brief="Sends the latest deleted messages.",
        help="Sends the last 5 deleted messages in a specified channel.\nIf the channel isn't specified, it uses the current channel.",
    )
    @commands.has_permissions(
        manage_messages=True
    )  # needs to be able to delete messages to run the command
    async def snipe(
        self, ctx: commands.Context, channel: discord.TextChannel = None, /
    ) -> None:
        if channel is None:
            channel = (
                ctx.channel
            )  # i am not checking if the channel is in the current server, since this bot is for a private server

        logs = self.sniped[channel.id]

        if not logs:
            await ctx.reply(
                f"There are no messages to be sniped in {'this channel.' if channel.id == ctx.channel.id else channel.mention}"
            )
            return

        embed = discord.Embed(
            title=f"Showing last 5 deleted messages for {'the current channel' if ctx.channel.id == channel.id else channel}",
            description="The lower the number is, the more recent it got deleted.",
            color=self.bot.embed_color,
        )
        zwsp = "\uFEFF"
        for i, log in reversed(list(enumerate(logs))):
            message, ts = log
            embed.add_field(
                name=str(i) + ("" if i else " (latest)"),
                value=f"""
    Author: {message.author.mention} (ID: {message.author.id}, Plain: {discord.utils.escape_markdown(str(message.author))})
    Deleted at: <t:{ts}:F> (Relative: <t:{ts}:R>)
    Content:
    ```
    {message.content.replace('`', f'{zwsp}`{zwsp}')}
    ```
    """,
                inline=False,
            )


        await ctx.reply(embed=embed)


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(Miscellanious(bot))
