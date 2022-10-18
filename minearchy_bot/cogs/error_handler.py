from __future__ import annotations

from contextlib import suppress as suppress_error
from traceback import format_exception as format_exit
from typing import TYPE_CHECKING

from discord import HTTPException
from discord.ext.commands import (
    ChannelNotFound,
    Cog,
    CommandNotFound,
    MissingPermissions,
    MissingRequiredArgument,
    NoPrivateMessage,
    NotOwner,
    TooManyArguments,
)

if TYPE_CHECKING:
    from discord.ext.commands import CommandError, Context

    from ..core import MinearchyBot


class ErrorHandler(Cog):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError) -> None:
        if hasattr(ctx.command, "on_error"):
            return

        if cog := ctx.cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (CommandNotFound,)
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, NoPrivateMessage):
            with suppress_error(HTTPException):
                await ctx.author.send(
                    f"The command `{ctx.command.qualified_name}` cannot be used in DMs."
                )

        elif isinstance(error, (MissingPermissions, NotOwner)):
            await ctx.reply("You can't use this command!")

        elif isinstance(error, MissingRequiredArgument):
            await ctx.reply(f"Missing a required argument: `{error.param.name}`.")

        elif isinstance(error, TooManyArguments):
            await ctx.reply("Too many arguments.")

        elif isinstance(error, ChannelNotFound):
            await ctx.reply("Invalid channel.")

        else:
            trace = "".join(format_exit(type(error), error, error.__traceback__))
            print(f"Ignoring exception in command {ctx.command}:\n{trace}")
            await self.bot.log_webhook.send(f"<@512640455834337290>```{trace}```")


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(ErrorHandler(bot))
