from __future__ import annotations

from datetime import timedelta as TimeDelta
from inspect import cleandoc as strip
from platform import python_version
from time import time as get_time
from typing import TYPE_CHECKING

from discord.ext.commands import Cog, command


if TYPE_CHECKING:
    from discord import Message
    from discord.ext.commands import Context

    from .. import MinearchyBot


class Miscellaneous(
    Cog,
    name = "Miscellaneous",
    description = "Miscellaneous commands.",
):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot
        self.bot.help_command.cog = self

    def cog_unload(self) -> None:
        self.bot.help_command.cog = None
        self.bot.help_command.hidden = True

    @command(
        brief = "Sends the GitHub repository link for the bot.",
        help = "Sends the GitHub repository link for the bot.",
    )
    async def github(self, ctx: Context) -> None:
        # Not a button since I want the embed.
        await ctx.reply("https://github.com/RGBCube/minearchy-bot")

    @command(
        brief = "Sends info about the bot.",
        help = "Sends info about the bot."
    )
    async def info(self, ctx: Context) -> None:
        await ctx.reply(
            strip(
                f"""
            __**Bot Info**__
            **Python Version:** v{python_version()}
            **Uptime:** `{TimeDelta(seconds = int(get_time() - self.bot.ready_timestamp))}`
            """
            )
        )

    @command(
        brief = "Sets you as AFK.",
        help = "Sets you as AFK.",
    )
    async def afk(self, ctx: Context) -> None:
        # No error because it will un-afk the caller.
        if ctx.author.display_name.lower().startswith("[AFK]"):
            return

        if ctx.me.top_role.position <= ctx.author.top_role.position:
            await ctx.reply(
                "I cannot set you as AFK because my role is lower than yours."
                "You can edit your nickname to set yourself as AFK (Add [AFK] to the start of it.)."
            )
            return

        await ctx.author.edit(nick = f"[AFK] {ctx.author.display_name}"[:32])
        await ctx.reply("Set your status to AFK. You can now touch grass freely 🌲.")

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.author.display_name.upper().startswith("[AFK]"):
            return

        await message.author.edit(nick = message.author.display_name[5:])
        await message.channel.send(
            f"Welcome back {message.author.mention}! I've unset your AFK status."
        )


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(Miscellaneous(bot))
