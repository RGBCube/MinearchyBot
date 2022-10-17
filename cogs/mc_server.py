from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from bot import MinearchyBot


class MinecraftServer(
    commands.Cog,
    name="Minecraft Server",
    description="Utilities for the Minecraft server.",
):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot

    @commands.group(
        invoke_without_command=True,
        brief="Sends the server IP.",
        help="Sends the server IP.",
    )
    async def ip(self, ctx: commands.Context) -> None:
        await ctx.reply(
            f"Java edition IP: `{self.bot.mc_server.ip}`\nBedrock edition IP:"
            f" `{self.bot.mc_server.bedrock_ip}` (Port: 19132)\nNote: Minecraft 1.18+"
            " is required to join."
        )

    @ip.command(brief="Sends the Java edition IP.", help="Sends the Java edition IP.")
    async def java(self, ctx: commands.Context) -> None:
        await ctx.reply(
            "The IP to connect on Minecraft Java edition is"
            f" `{self.bot.mc_server.ip}`\nNote: Minecraft 1.18+ is required to join."
        )

    @ip.command(
        brief="Sends the Bedrock edition IP.",
        help="Sends the Bedrock edition IP.",
    )
    async def bedrock(self, ctx: commands.Context) -> None:
        await ctx.reply(
            "The IP to connect on Minecraft Bedrock edition is"
            f" `{self.bot.mc_server.bedrock_ip}` (Port: 19132)\nNote: Minecraft 1.18+"
            " is required to join."
        )

    @commands.command(
        brief="Shows information about the Minecraft server.",
        help=(
            "Shows the total player count, the Minecraft server IP and the server"
            " latency."
        ),
    )
    async def status(self, ctx: commands.Context) -> None:
        server = self.bot.mc_server
        status = server.status()
        await ctx.reply(
            f"The server with the IP `{server.ip}` has {status.players.online} "
            f"players and responded in `{int(status.latency)}ms`"
        )

    @commands.command(
        brief="Sends the link to the wiki.", help="Sends the link to the wiki."
    )
    async def wiki(self, ctx: commands.Context) -> None:
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Go to the wiki!",
                url="https://landsofminearchy.com/wiki",
            )
        )
        await ctx.reply(view=view)

    @commands.command(
        brief="Sends the link to the store.",
        help="Sends the link to the store.",
    )
    async def store(self, ctx: commands.Context) -> None:
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Go to the store!",
                url="https://landsofminearchy.com/store",
            )
        )
        await ctx.reply(view=view)

    @commands.command(
        brief="Sends the links you can use to vote for the Minecraft server.",
        help="Sends the links you can use to vote for the Minecraft server.",
    )
    async def vote(self, ctx: commands.Context) -> None:
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Vote for the Minecraft server!",
                url="https://landsofminearchy.com/vote",
            )
        )
        await ctx.reply(view=view)

    @commands.command(
        aliases=["apply", "staffapply", "applystaff", "applyforstaff", "staff-application", "staff-applications", "staff_applications"],
        brief="Sends the link to the staff application.",
        help="Sends the link to the staff application.",
    )
    async def staff_application(self, ctx: commands.Context) -> None:
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Apply for staff!",
                url="https://docs.google.com/forms/d/1I7Rh_e-ZTXm5L51XoKZsOAk7NAJcHomUUCuOlQcARvY/viewform",
            )
        )
        await ctx.reply(view=view)


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(MinecraftServer(bot))
