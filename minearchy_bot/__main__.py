from __future__ import annotations

import json
from os import environ as env
from pathlib import Path

from . import MinearchyBot


def main() -> None:
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

    bot.run()

if __name__ == "__main__":
    main()
