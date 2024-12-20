#!/usr/bin/env python3


from dotenv import load_dotenv
from .cog import *
import os
import asyncio


def main():
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    prefix = os.getenv("PREFIX", '#')

    assert token

    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True

    client = commands.Bot(command_prefix=prefix, intents=intents)
    asyncio.run(client.add_cog(UltraTicTacCog(client)))
    client.run(token)


if __name__ == "__main__":
    main()
