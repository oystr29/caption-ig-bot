# Instagram Caption Bot

This is an instagram caption bot that let you to change your caption to display your current **like count*,
and **play count**. Mostly inspired by [Tom Scoot](https://www.youtube.com/watch?v=BxV14h0kFs0) and [Bed Awwad](https://youtu.be/RxkLFAGetVQ?si=GaVFy2J2MMHrFlLu)

## Prerequisites

Make sure you have all of the depedencies.

### Python

Install [python](https://www.python.org/) first.

### Instagrapi

This is the [core library](https://subzeroid.github.io/instagrapi/) of this program. It lets you to send a request and get a response from instagram private api.

Install it using [pip](https://pip.pypa.io/en/stable/installation/). Also install pillow and python-dotenv cuz we also need that.

```bash
pip install instagrapi pillow python-dotenv
```

## Setup

First clone this repo.

```bash
git clone https://github.com/oystr29/caption-ig-bot
cd caption-ig-bot
```

Make all neccessary files.

```bash
cp .env.example .env
cp app.example.log app.log
cp session.example.json session.json
```

You can ignore `app.log` and `session.json`, but you must fill all the variables in `.env`

```bash
IG_USERNAME=''
IG_PASSWORD=''
TELE_TOKEN=""
TELE_CHAT_ID=""
```

You need to make a telegram bot to send a notification if the program crash.

## Run it

Simply call python with the filename 

```bash
python main.py
```

or if you wanna run it on the background (also work on server)

```bash
python main & # Only work on unix system (not windows)
```
