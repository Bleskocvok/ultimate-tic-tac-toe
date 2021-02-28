#!/usr/bin/env python3


from dotenv import load_dotenv
from cog import *
import os


def main():
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    prefix = os.getenv("PREFIX", '!')

    client = commands.Bot(command_prefix=prefix)
    client.add_cog(UltraTicTacCog(client))
    client.run(token)


if __name__ == "__main__":
    main()
