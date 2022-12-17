from __future__ import annotations

from collections import defaultdict as DefaultDict, deque as Deque
from datetime import timedelta as TimeDelta
from inspect import cleandoc as strip
from time import time as get_time
from typing import TYPE_CHECKING

from discord import Color, Embed, TextChannel
from discord.ext import commands
from discord.ext.commands import Cog, command
from discord.utils import escape_markdown

if TYPE_CHECKING:
    from discord import Member, Message
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
        self.sniped = DefaultDict(Deque)

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

    @command(
        brief="Sends the latest deleted messages.",
        help=(
            "Sends the last 5 deleted messages in a specified channel.\nIf the channel"
            " isn't specified, it uses the current channel."
        ),
    )
    @commands.has_permissions(manage_messages=True)  # needs to be able to delete messages to run the command
    async def snipe(self, ctx: Context, channel: TextChannel | None = None) -> None:
        if channel is None:
            channel = ctx.channel

        logs = self.sniped[channel.id]

        if not logs:
            await ctx.reply(
                "There are no messages to be sniped in"
                f" {'this channel.' if channel.id == ctx.channel.id else channel.mention}"
            )
            return

        embed = Embed(
            title=(
                "Showing last 5 deleted messages for"
                f" {'the current channel' if ctx.channel.id == channel.id else channel}"
            ),
            description="The lower the number is, the more recent it got deleted.",
            color=Color.random(),
        )

        zwsp = "\uFEFF"

        for i, log in reversed(list(enumerate(logs))):
            message, ts = log

            embed.add_field(
                name=str(i) + ("" if i else " (latest)"),
                value=strip(
                    f"""
                    Author: {message.author.mention} (ID: {message.author.id}, Plain: {escape_markdown(str(message.author))})
                    Deleted at: <t:{ts}:F> (Relative: <t:{ts}:R>)
                    Content:
                    ```
                    {message.content.replace('`', f'{zwsp}`{zwsp}')}
                    ```
                    """
                ),
                inline=False,
            )

        await ctx.reply(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message: Message) -> None:
        if not message.guild:
            return

        self.sniped[message.channel.id].appendleft((message, int(get_time())))

        while len(self.sniped[message.channel.id]) > 5:
            self.sniped[message.channel.id].pop()


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(Moderation(bot))
