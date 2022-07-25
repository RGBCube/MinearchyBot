from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from bot import MinearchyBot


class Suggestions(
    commands.Cog,
    name="Suggestions",
    description="Suggest stuff.",
):
    def __init__(self, bot: MinearchyBot) -> None:
        self.bot = bot

    @commands.command(brief="Make a suggestion.", help="Make a suggestion.")
    async def suggest(self, ctx: commands.Context, *, suggestion: str) -> None:
        embed = (
            discord.Embed(
                title=f"Suggestion from {ctx.author}",
                description=suggestion,
                color=self.bot.embed_color,
            )
            .set_thumbnail(url=ctx.author.display_avatar.url)
            .set_footer(text="=suggest <suggestion>")
        )

        message = await self.bot.suggestions_channel.send(embed=embed)

        await message.add_reaction("✅")
        await message.add_reaction("❌")

        await ctx.reply(
            "Suggestion submitted!\nYou can view it at"
            f" {self.bot.suggestions_channel.mention}"
        )


async def setup(bot: MinearchyBot) -> None:
    await bot.add_cog(Suggestions(bot))
