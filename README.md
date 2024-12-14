# ultimate-tic-tac-toe

![testing badge](https://github.com/Bleskocvok/ultimate-tic-tac-toe/actions/workflows/tests.yml/badge.svg)

```sh
git clone https://github.com/Bleskocvok/ultimate-tic-tac-toe
cd ultimate-tic-tac-toe
pip3 install -r requirements.txt

```

You will also need to have a `discord` token prepared in a `.env` file like
this. In the `discord` developer portal, you also need to have selected
“message content” intent.
```
$ cat .env
DISCORD_TOKEN=XXXXX...XXX
```

If all is setup correctly, the bot can be started by running the `main.py` file.
```sh
python3 src/main.py
```

In a channel where your bot has been added, simply type `!help` to see how to
play the game.

A player can start a match against another user using command `!start @USER`
