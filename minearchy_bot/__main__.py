from __future__ import annotations

import asyncio
from os import environ as env

from . import MinearchyBot


async def async_main() -> None:
    env[f"JISHAKU_HIDE"] = "True"
    env[f"JISHAKU_NO_UNDERSCORE"] = "True"

    bot = MinearchyBot(
        token = env["MINEARCHY_BOT_TOKEN"],
        webhook_url = env["MINEARCHY_BOT_WEBHOOK_URL"]
    )

    await bot.run()

def main() -> None:
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
