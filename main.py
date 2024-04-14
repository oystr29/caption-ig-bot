import logging
import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

dirname = os.path.dirname(__file__)

logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
    filename=os.path.join(dirname, "app.log"),
)
log = logging.getLogger()
load_dotenv()


USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

sesh_path = os.path.join(dirname, "session.json")
print(sesh_path)

cl = Client()


def send_to_telegram(message):

    apiToken = os.getenv("TELE_TOKEN")
    chatID = os.getenv("TELE_CHAT_ID")
    apiURL = f"https://api.telegram.org/bot{apiToken}/sendMessage"

    try:
        response = requests.post(apiURL, json={"chat_id": chatID, "text": message})
        print(response.text)
    except Exception as e:
        print(e)


def login():
    logging.info("Load Settings...")
    session = cl.load_settings(sesh_path)

    login_via_session = False
    login_via_password = False

    if session:
        try:
            logging.info("Set Settings")
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            try:
                logging.info("Check If Login")
                cl.account_info().username
            except LoginRequired:
                send_to_telegram("Session Invalid, login with password...")
                log.info("Session Invalid, login with password...")

                old_session = cl.get_settings()

                # NOTE use the same devices uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            send_to_telegram(f"Couldnt login with session: {e}")
            log.error("Couldnt login with session: %s" % e)

    if not login_via_session:
        try:
            log.info("Try to login via username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_password = True
        except Exception as e:
            send_to_telegram(f"Couldnt login with username and password: {e}")
            log.error("Couldnt login with username and password")

    if not login_via_session and not login_via_password:
        send_to_telegram("Couldnt login")
        raise Exception("Couldn't login")


login()

logging.info("Dump Settings")
cl.dump_settings(sesh_path)

temp_likes = 0
temp_plays = 0

logging.info("Get Account Info")
account = cl.account_info()

run = True
while run:
    try:

        logging.info("Get Reels")
        reels = cl.user_clips(account.pk, amount=1)

        logging.info("Get First Reels")
        first_reel = reels[0]

        date_str = f"{datetime.now():%Y-%m-%d %H:%M:%S%z}"
        caption = f"likes: {first_reel.like_count}\nplays: {first_reel.play_count}\nlast: {date_str}"

        if temp_likes != first_reel.like_count or temp_plays != first_reel.play_count:
            logging.info(f"{temp_likes},{first_reel.like_count} = old_like, new_likes")
            logging.info(f"{temp_plays},{first_reel.play_count} = old_play, new_plays")
            cl.media_edit(first_reel.id, caption)
            temp_likes = first_reel.like_count
            temp_plays = first_reel.play_count
            logging.info("Done Change Caption")
        else:
            logging.info("No Changes, skip media edit")
        logging.info("-----------Iteration---------------")
        time.sleep(60)
    except Exception as e:
        err = f"Error: {e}"
        logging.error(err)
        send_to_telegram(err)
        run = False
        raise Exception(err)
