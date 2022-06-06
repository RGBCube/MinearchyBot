from __future__ import annotations

from typing import TYPE_CHECKING
from discord.ext import commands
import discord

if TYPE_CHECKING:
    from bot import MinearchyBot


class MinecraftServer(
    commands.Cog,
    name="Minecraft Server",
    description="Utilites for the Minecraft server.",
):
    def __init__(self, bot: MinearchyBot, /) -> None:
        self.bot = bot

    @commands.group(
        invoke_without_command=True,
        brief="Sends the server IP.",
        help="Sends the server IP.",
    )
    async def ip(self, ctx: commands.Context, /) -> None:
        await ctx.reply(
            f"Java edition IP: `{self.bot.mc_server.ip}`\nBedrock edition IP: `{self.bot.mc_server.bedrock_ip}`"
        )

    @ip.command(
        brief="Sends the Java edition IP.", help="Sends the Java edition IP."
    )
    async def java(self, ctx: commands.Context, /) -> None:
        await ctx.reply(
            f"The IP to connect on Minecraft Java edition is `{self.bot.mc_server.ip}`"
        )

    @ip.command(
        brief="Sends the Bedrock edition IP.",
        help="Sends the Bedrock edition IP.",
    )
    async def bedrock(self, ctx: commands.Context, /) -> None:
        await ctx.reply(
            f"The IP to connect on Minecraft Bava edition is `{self.bot.mc_server.ip}`"
        )

    @commands.command(
        brief="Shows information about the Minecraft server.",
        help="Shows the total player count, the Minecraft server IP and the server latency.",
    )
    async def status(self, ctx: commands.Context, /) -> None:
        server = self.bot.mc_server
        status = server.status()
        await ctx.reply(
            f"The server with the IP `{server.ip}` has {status.players.online} "
            f"players and responded in `{int(status.latency)}ms`"
        )

    @commands.command(
        brief="Sends the link to the wiki.", help="Sends the link to the wiki."
    )
    async def wiki(self, ctx: commands.Context, /) -> None:
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Go to the wiki!",
                url="https://www.landsofminearchy.com/wiki",
            )
        )
        await ctx.reply(view=view)

    @commands.command(
        brief="Sends the link to the store.",
        help="Sends the link to the store.",
    )
    async def store(self, ctx: commands.Context, /) -> None:
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Go to the store!",
                url="https://www.landsofminearchy.com/store",
            )
        )
        await ctx.reply(view=view)


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(MinecraftServer(bot))
