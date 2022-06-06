from __future__ import annotations

from typing import TYPE_CHECKING
from discord.ext import commands
import discord
import sys
import traceback

if TYPE_CHECKING:
    from bot import MinearchyBot


class ErrorHandler(commands.Cog):
    def __init__(self, bot: MinearchyBot, /) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError, /
    ) -> None:
        if hasattr(ctx.command, "on_error"):
            return

        if cog := ctx.cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound,)
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f"The commmand `{ctx.command}` cannot be used in DMs."
                )
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("You can't use this command!")

        else:
            trace = traceback.format_exception(
                type(error), error, error.__traceback__
            )
            print(f"Ignoring exception in command {ctx.command}:\n{trace}")
            await self.bot.log_webhook.send(
                f"<@512640455834337290>```{trace}```"
            )


async def setup(bot: MinearchyBot, /) -> None:
    await bot.add_cog(ErrorHandler(bot))
