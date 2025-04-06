from __future__ import annotations

import asyncio
import json
from os import environ as env
from pathlib import Path

from . import MinearchyBot


async def main() -> None:
    config = json.loads(
        (
            Path(__file__).parent / "config.json"
        ).read_text()
    )

    env[f"JISHAKU_HIDE"] = "True"
    env[f"JISHAKU_NO_UNDERSCORE"] = "True"

    bot = MinearchyBot(
        token = config["BOT_TOKEN"],
        webhook_url = config["WEBHOOK_URL"]
    )

    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
