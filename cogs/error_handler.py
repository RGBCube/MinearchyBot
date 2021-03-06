from __future__ import annotations

import contextlib
import traceback
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from bot import MinearchyBot


class ErrorHandler(commands.Cog):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
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
            with contextlib.suppress(discord.HTTPException):
                await ctx.author.send(
                    f"The command `{ctx.command.qualified_name}` cannot be used in DMs."
                )

        elif isinstance(error, (commands.MissingPermissions, commands.NotOwner)):
            await ctx.reply("You can't use this command!")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Missing a required argument: `{error.param.name}`.")

        elif isinstance(error, commands.TooManyArguments):
            await ctx.reply("Too many arguments.")

        elif isinstance(error, commands.ChannelNotFound):
            await ctx.reply("Invalid channel.")

        else:
            trace = "".join(
                traceback.format_exception(type(error), error, error.__traceback__)
            )
            print(f"Ignoring exception in command {ctx.command}:\n{trace}")
            await self.bot.log_webhook.send(f"<@512640455834337290>```{trace}```")


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(ErrorHandler(bot))
