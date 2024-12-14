# ultimate-tic-tac-toe

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

You will need to have a `discord` token prepared in a `.env` file like
this. In the `discord` developer portal, you also need to have selected
“message content” intent.
```
$ cat .env
DISCORD_TOKEN=XXXXX...XXX
```

If all is setup correctly, the bot can be started by running the `bot.py` file.
```sh
python3 src/bot.py
```

In a channel where your bot has been added, simply type `!help` to see how to
play the game.

A player can start a match against another user using command `!start @USER`


## Running in terminal

For testing purposes, the game can also be run in the terminal, against a
simple AI or in hot-seat mode against another player. Run the `play.py` file to
play the game in the terminal.
```sh
python3 src/play.py
```
