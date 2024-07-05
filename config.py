import os
from genshin import Game
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCOUNTS = (
  {
    "ltuid_v2": os.environ.get("MY_UID"),
    "ltmid_v2": os.environ.get("MY_MID"),
    "ltoken_v2": os.environ.get("MY_TOKEN"),
    "games": [ Game.GENSHIN, Game.ZZZ]
  },
  {
    "ltuid_v2": os.environ.get("ALT_UID"),
    "ltmid_v2": os.environ.get("ALT_MID"),
    "ltoken_v2": os.environ.get("ALT_TOKEN"),
    "games": [ Game.STARRAIL ]
  }
)

WEBHOOK = {
  "url": os.environ.get("WEBHOOK_URL"),
  "username": os.environ.get("WEBHOOK_NAME"),
  "avatar": os.environ.get("WEBHOOK_AVATAR")
}