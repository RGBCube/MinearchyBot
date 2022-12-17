from __future__ import annotations

from io import BytesIO
from time import monotonic as get_monotonic
from typing import TYPE_CHECKING

from discord import (
    CategoryChannel,
    File,
    ForumChannel,
    Member,
    Role,
    StageChannel,
    TextChannel,
    VoiceChannel,
)
from discord.ext.commands import Cog, command

if TYPE_CHECKING:
    from discord.ext.commands import Context

    from .. import MinearchyBot


class Utils(Cog):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot

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
        name="channel-perm-tree",
        hidden=True
    )
    async def channel_perm_tree(self, ctx: Context) -> None:
        string = []

        for channel in ctx.guild.channels:
            # Only root level channels.
            if getattr(channel, "category", False):
                continue

            if isinstance(channel, CategoryChannel):
                string.append(f"category {channel.name}:")
                string.append(f"  id: {channel.id}")

                for thing, overwrites in channel.overwrites.items():
                    if isinstance(thing, Role):
                        typ = "role"
                        name = thing.name
                    if isinstance(thing, Member):
                        typ = "member"
                        name = f"{thing.name}#{thing.discriminator}"
                    else:
                        typ = repr(thing.type)
                        name = "unknown"

                    string.append(f"    {typ} {name}:")
                    string.append(f"    id: {thing.id}")

                    allow, deny = [], []

                    for perm, value in overwrites._values.items():
                        if value is True:
                            allow.append(perm)
                        elif value is False:
                            deny.append(perm)

                    if allow or deny:
                        string.append("    permissions:")

                        for a in allow:
                            string.append(f"      {a}: ✅")
                        for d in deny:
                            string.append(f"      {d}: ❌")

                    string.append("    channels:")

                    for child in channel.channels:
                        if isinstance(child, TextChannel):
                            typ = "text"
                        elif isinstance(child, ForumChannel):
                            typ = "forum"
                        elif isinstance(child, VoiceChannel):
                            typ = "voice"
                        elif isinstance(child, StageChannel):
                            typ = "stage"
                        else:
                            typ = "unknown"

                        string.append(f"      {typ} channel `{child.name}`:")
                        string.append(f"        id: {child.id}")

                        for child_thing, child_overwrites in child.overwrites.items():
                            if isinstance(child_thing, Role):
                                typ = "role"
                                name = child_thing.name
                            if isinstance(child_thing, Member):
                                typ = "member"
                                name = f"{child_thing.name}#{child_thing.discriminator}"
                            else:
                                typ = repr(child_thing.type)
                                name = "unknown"

                            string.append(f"          {typ} {name}:")
                            string.append(f"          id: {child_thing.id}")

                            allow, deny = [], []

                            for perm, value in overwrites._values.items():
                                channel_corresponding_value = child_overwrites._values.get(perm)

                                unique = value is not channel_corresponding_value
                                if not unique:
                                    continue

                                if value is True:
                                    allow.append(perm)
                                elif value is False:
                                    deny.append(perm)

                            if allow or deny:
                                string.append("          permissions:")

                                for a in allow:
                                    string.append(f"            {a}: ✅")
                                for d in deny:
                                    string.append(f"            {d}: ❌")

            else:
                if isinstance(channel, TextChannel):
                    typ = "text"
                elif isinstance(channel, ForumChannel):
                    typ = "forum"
                elif isinstance(channel, VoiceChannel):
                    typ = "voice"
                elif isinstance(channel, StageChannel):
                    typ = "stage"
                else:
                    typ = "unknown"

                string.append(f"{typ} channel `{channel.name}`:")
                string.append(f"  id: {channel.id}")

                for thing, overwrites in channel.overwrites.items():
                    if isinstance(thing, Role):
                        typ = "role"
                        name = thing.name
                    if isinstance(thing, Member):
                        typ = "member"
                        name = f"{thing.name}#{thing.discriminator}"
                    else:
                        typ = repr(thing.type)
                        name = "unknown"

                    string.append(f"    {typ} {name}:")
                    string.append(f"    id: {thing.id}")

                    allow, deny = [], []

                    for perm, value in overwrites._values.items():
                        if value is True:
                            allow.append(perm)
                        elif value is False:
                            deny.append(perm)

                    if allow or deny:
                        string.append("    permissions:")

                        for a in allow:
                            string.append(f"      {a}: ✅")
                        for d in deny:
                            string.append(f"      {d}: ❌")

        await ctx.reply(
            file=File(
                BytesIO("\n".join(string).encode()),
                filename="channel-perm-tree.txt"
            )
        )


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(Utils(bot))
