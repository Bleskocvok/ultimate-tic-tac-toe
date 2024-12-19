# ultimate-tic-tac-toe

<div align="center">
    <img width="128" height="128" src="icon.png" alt="icon">
    <!-- ![icon](icon.png) -->
</div>

![testing badge](https://github.com/Bleskocvok/ultimate-tic-tac-toe/actions/workflows/tests.yml/badge.svg)

## Running the code

```sh
git clone https://github.com/Bleskocvok/ultimate-tic-tac-toe
cd ultimate-tic-tac-toe
pip3 install -r requirements.txt
```

## Discord bot

The primary focus of this project is a discord bot for playing
Ultimate-Tic-Tac-Toe. Below is a brief outline for setting up your own instance
of this discord bot.

You will need to have a `discord` token prepared in a `DISCORD_TOKEN`
environment variable. The simplest way to set it up is to create a `.env` file
placed in the project directory.
```sh
$ cat .env
DISCORD_TOKEN=XXXXX...XXX
```

In the discord developer portal where you have created your bot and generated
the token, you also need to chose the correct permissions.

#### Scopes

- bot

#### Bot permissions (`10304`)

- Send messages
- Manage messages (remove reactions)
- Add reactions

#### Privileged Gateway Intents

- Message content intent

If all is setup correctly, the bot can be started by running the `bot.py` file.
```sh
python3 -m src.bot
```

In a channel where your bot has access, simply type `#help` to see how to play
the game. The commands `#rules` and `#example` provide an explanation of the
rules and `#start_bot_vs_bot` shows a game of the bot against itself play out.

A player can start a match against another user using command `#start @USER`.
It is also possible to enter only `#start` in which case the match will start
against the bot itself which uses a simple “AI” to play turns.

The `#` command prefix can be changed by setting the `PREFIX` environment
variable, which can be don in your `.env` file. If setup the following way, the
prefix would be `!`.
```sh
$ cat .env
DISCORD_TOKEN=XXXXX...XXX
PREFIX=!
```

## Running in terminal

For testing purposes, the game can also be run in the terminal, against a simple
AI or in hot-seat mode against another player. Run the `play.py` file from a
terminal to start the game.
```sh
python3 -m src.play
```

## Demo

![demo recording](../demo/demo.gif?raw=true)
