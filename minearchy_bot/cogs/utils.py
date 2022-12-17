from __future__ import annotations

from io import BytesIO
from time import monotonic as get_monotonic
from typing import TYPE_CHECKING

from discord import CategoryChannel, File
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


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(Utils(bot))
