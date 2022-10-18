from __future__ import annotations

from json import load as parse_json
from os import environ as env
from pathlib import Path

from uvloop import install as install_uvloop

from . import MinearchyBot

install_uvloop()

with (Path(__file__).parent.parent / "config.json").open() as f:
    config = parse_json(f)

for key in ("HIDE", "NO_UNDERSCORE"):
    env[f"JISHAKU_{key}"] = "True"

bot = MinearchyBot(token=config["BOT_TOKEN"], webhook_url=config["WEBHOOK_URL"])

bot.run()
