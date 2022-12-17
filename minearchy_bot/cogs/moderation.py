from __future__ import annotations

from datetime import timedelta as TimeDelta
from typing import TYPE_CHECKING

from discord.ext import commands
from discord.ext.commands import Cog, command

if TYPE_CHECKING:
    from discord import Member
    from discord.ext.commands import Context

    from .. import MinearchyBot


class Moderation(Cog):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot
        self.time_values = {
            "d": "days",
            "h": "hours",
            "m": "minutes",
            "s": "seconds",
        }

    @command(
        aliases=("mute",),
        brief="Times out a user.",
        help="Times out a user."
    )
    @commands.has_permissions(manage_messages=True)
    async def timeout(self, ctx: Context, member: Member, duration: str = "1d") -> None:
        if duration[-1] not in self.time_values or len(duration) < 2:
            await ctx.reply("Invalid duration. Valid durations are: d, h, m, s.")
            return

        try:
            time = int(duration[:-1])
        except ValueError:
            await ctx.reply("Invalid time.")
            return

        # days, hours, minutes, seconds
        clean_time_name = self.time_values[duration[-1]]

        # this is so cursed but works
        await member.timeout(
            TimeDelta(**{clean_time_name: time}), reason=f"Timed out by moderator {ctx.author}"
        )

        await ctx.reply(f"Timed out {member.mention} for {time} {clean_time_name}.")


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(Moderation(bot))
