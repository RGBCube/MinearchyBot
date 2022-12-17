from __future__ import annotations

from collections import defaultdict as DefaultDict, deque as Deque
from datetime import timedelta as TimeDelta
from inspect import cleandoc as strip
from io import BytesIO
from platform import python_version
from time import monotonic as get_monotonic, time as get_time
from typing import TYPE_CHECKING

from discord import CategoryChannel, Color, Embed, File, TextChannel
from discord.ext import commands
from discord.ext.commands import Cog, command
from discord.utils import escape_markdown

from ..utils import override

if TYPE_CHECKING:
    from discord import Message
    from discord.ext.commands import Context

    from .. import MinearchyBot


class Miscellaneous(
    Cog,
    name="Miscellaneous",
    description="Various utilities.",
):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot
        self.bot.help_command.cog = self
        self.sniped = DefaultDict(Deque)

    @override
    def cog_unload(self) -> None:
        self.bot.help_command.cog = None
        self.bot.help_command.hidden = True

    @command(brief="Hello!", help="Hello!")
    async def hello(self, ctx: Context) -> None:
        await ctx.reply(f"Hi {escape_markdown(ctx.author.name)}, yes the bot is running :).")

    @command(
        brief="Sends the total members in the server.",
        help="Sends the total members in the server.",
    )
    async def members(self, ctx: Context) -> None:
        await ctx.reply(f"There are `{ctx.guild.member_count}` users in this server.")

    @command(
        brief="Sends the bots ping.",
        help="Sends the bots ping."
    )
    async def ping(self, ctx: Context) -> None:
        ts = get_monotonic()
        message = await ctx.reply("Pong!")
        ts = get_monotonic() - ts
        await message.edit(content=f"Pong! `{int(ts * 1000)}ms`")

    @command(
        brief="Sends info about the bot.",
        help="Sends info about the bot."
    )
    async def info(self, ctx: Context) -> None:
        await ctx.reply(
            strip(
                f"""
            __**Bot Info**__
            **Python Version:** v{python_version()}
            **Uptime:** `{TimeDelta(seconds=int(get_time() - self.bot.ready_timestamp))}`
            """
            )
        )

    @command(
        name="channel-perm-tree",
        hidden=True
    )
    async def channel_perm_tree(self, ctx: Context) -> None:
        string = []

        for channel in ctx.guild.channels:
            ind = "    "
            ind_nr = 1 if getattr(channel, "category", False) else 0

            string.append(ind*ind_nr + f"{'category' if isinstance(channel, CategoryChannel) else 'channel'} {channel.name}:")

            if channel.permissions_synced:
                string.append(ind*(ind_nr+1) + "permissions: synced")
            else:
                string.append(ind*(ind_nr+1) + "permissions:")

                if not channel.category:
                    for thing, overwrites in channel.overwrites.items():
                        allows, denies = overwrites.pair()

                        for allow in allows:
                            string.append(ind*(ind_nr+2) + f"{allow[0]}: ✅")
                        for deny in denies:
                            string.append(ind*(ind_nr+2) + f"{deny[0]}: ❌")

                else:
                    for thing, overwrites in channel.overwrites.items():
                        parent_overwrites = channel.category.overwrites.get(thing)

                        allows, denies = overwrites.pair()
                        parent_allows, parent_denies = parent_overwrites.pair() if parent_overwrites else ((), ())

                        for allow in allows:
                            if allow not in parent_allows:
                                string.append(ind*(ind_nr+2) + f"{allow[0]}: ✅")

                        for deny in denies:
                            if deny not in parent_denies:
                                string.append(ind*(ind_nr+2) + f"{deny[0]}: ❌")

        await ctx.reply(
            file=File(
                BytesIO("\n".join(string).encode()),
                filename="channel-perm-tree.txt"
            )
        )

    @command(
        brief="Sets you as AFK.",
        help="Sets you as AFK.",
    )
    async def afk(self, ctx: Context) -> None:
        # no error cuz it will un-afk them
        if ctx.author.display_name.lower().startswith("[AFK]"):
            return

        if ctx.me.top_role.position <= ctx.author.top_role.position:
            await ctx.reply(
                "I cannot set you as AFK because my role is lower than yours."
                "You can edit your nickname to set yourself as AFK (Add [AFK] to the start of it.)."
            )
            return

        await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}"[:32])
        await ctx.reply("Set your status to AFK. You can now touch grass freely 🌲.")

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.author.display_name.upper().startswith("[AFK]"):
            return

        await message.author.edit(nick=message.author.display_name[5:])
        await message.channel.send(f"Welcome back {message.author.mention}! I've unset your AFK status.")

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
    await bot.add_cog(Miscellaneous(bot))
