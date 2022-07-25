from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from datetime import timedelta
from typing import Optional

if TYPE_CHECKING:
    from bot import MinearchyBot


class Moderation(commands.Cog):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot

    @commands.command(
        aliases=["mute"],
        brief="Times out a user.",
        help="Times out a user."
    )
    @commands.has_permissions(manage_messages=True)
    async def timeout(self, ctx: commands.Context, member: discord.Member, duration: Optional[str]) -> None:
        times = {
            "d": "days",
            "h": "hours",
            "m": "minutes",
            "s": "seconds",
        }
        if duration is None:
            duration = "1d"
        if duration[-1] not in times or len(duration) < 2:
            await ctx.reply("Invalid duration. Valid durations are: d, h, m, s.")
            return
        try:
            time = int(duration[:-1])
        except ValueError:
            await ctx.reply("Invalid time.")
            return

        clean_time_name = times[duration[-1]]
        await member.timeout(timedelta(**{clean_time_name: time}), reason=f"Timed out by moderator {ctx.author}")
        await ctx.send(f"Timed out {member.mention} for {time} {clean_time_name}.")


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(Moderation(bot))
