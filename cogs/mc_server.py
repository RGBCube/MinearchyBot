from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands, tasks
import subprocess
import psutil

if TYPE_CHECKING:
    from bot import MinearchyBot


class MinecraftServer(
    commands.Cog,
    name="Minecraft Server",
    description="Utilites for the Minecraft server.",
):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        self.check_processes_up.start()

    async def cog_unload(self) -> None:
        self.check_processes_up.cancel()

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
                url="https://www.landsofminearchy.com/wiki",
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
                url="https://www.landsofminearchy.com/store",
            )
        )
        await ctx.reply(view=view)

    @tasks.loop(minutes=5)
    async def check_processes_up(self) -> None:
        pass
        # pids = [
        #     int(pid)
        #     for pid in subprocess.Popen(
        #         ["ps", "aux", "|", "grep", "java"], stdout=subprocess.PIPE
        #     )
        #     .communicate()[0]
        #     .splitlines()
        # ]
        # await self.bot.log_webhook.send(f"```\n{pids!r}```")
        #
        # for pid in pids:
        #     if not psutil.pid_exists(pid):
        #         await self.bot.log_webhook.send(f"No such pid: {pid}")


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(MinecraftServer(bot))
