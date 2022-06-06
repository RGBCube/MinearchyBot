# Minearchy Bot
This is a simple bot made for the [Minearchy Discord](https://discord.gg/2n6T78JS9k) server.

## Installing
1: Clone this repo and `cd` into it.

2: Edit the `config.example.json` to your liking and rename it to `config.json`.

3: If you are using replit, set the `USING_REPLIT` variable to `true` (or any non-empty string works, really).

4: Run `python bot.py`.

## Commands

### Minecraft Server Related Commands
`=ip [java|bedrock]`: Sends both of the server IPs. If the version is specified, it sends that versions IP.

`=status`: Sends the Minecraft servers player count and latency (ping).

`=store`: Sends a link to the store.

`=wiki`: Sends a link to the wiki.

### Miscellaneous Commands
`=count`: Sends how many servers the bot is in.

`=hello`: Hello!

`=help`: Sends bot help.

`=info`: Sends info about the bot. This is the bots Python runtime version and uptime.

`=ping`: Sends the bots latency.
    