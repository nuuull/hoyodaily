import genshin
import asyncio
import aiohttp
import datetime
from config import ACCOUNTS, WEBHOOK

async def main():
  discord_embeds = []
  for account in ACCOUNTS:
    cookies = { key: value for key, value in account.items() if key != "games" }
    client = genshin.Client(cookies)
    
    hoyolab_user = await client.get_hoyolab_user(account["ltuid_v2"])
      
    for game in account["games"]:
      try:
        await client.claim_daily_reward(game=game, reward=False)
      except genshin.AlreadyClaimed as e:
        result_value = "Daily reward already claimed"
        result_color = 15871
      else:
        result_value = "Daily checked in successfully"
        result_color = 56576

      info, rewards = await asyncio.gather(
        client.get_reward_info(game=game),
        client.get_monthly_rewards(game=game),
      )

      rewards_today = rewards[info.claimed_rewards - 1]
      rewards_tommorow = rewards[info.claimed_rewards]
      
      discord_embeds.append(build_embed({
        "game": game,
        "nickname": hoyolab_user.nickname,
        "result_value": result_value,
        "embed_color": result_color,
        "days_checked_in": info.claimed_rewards,
        "days_missing": info.missed_rewards,
        "reward_today": f"{rewards_today.name} {rewards_today.amount}x",
        "reward_icon": rewards_today.icon,
        "reward_tommorow": f"{rewards_tommorow.name} {rewards_tommorow.amount}x"
      }))
  
  data = await post_webhook(discord_embeds)
  print(data)

def build_embed(task_info):
  game_name, game_icon = get_game_info(task_info["game"])
  
  return {
    "title": "Daily Check-In Task",
    "description": task_info["result_value"], 
    "color": task_info["embed_color"],
    "thumbnail": {
      "url": task_info["reward_icon"]
    },
    "fields": [
      {
        "name": "HoYoLab User",
        "value": task_info["nickname"]
      },
      {
        "name": "Rewards Today",
        "value": task_info["reward_today"]
      },
      {
        "name": "Rewards Tommorow",
        "value": task_info["reward_tommorow"]
      },
      {
        "name": "Days Checked In",
        "value": str(task_info["days_checked_in"])
      },
      {
        "name": "Days Missing",
        "value": str(task_info["days_missing"])
      }
    ],
    "author": {
      "name": game_name,
      "icon_url": game_icon
    },
    "timestamp": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
  }

async def post_webhook(embeds):
  data = { 
    "username": WEBHOOK["username"],
    "avatar_url": WEBHOOK["avatar"],
    "embeds": embeds
  }
  async with aiohttp.ClientSession() as session:
    async with session.post(WEBHOOK["url"], json=data) as response:
      if response.status == 204:
        return await response.text()
      else:
        return None 

def get_game_info(game):
  if game == genshin.Game.HONKAI:
    return (
      "Honkai Impact 3rd",
      "https://fastcdn.hoyoverse.com/static-resource-v2/2024/02/29/3d96534fd7a35a725f7884e6137346d1_3942255444511793944.png"
    )
  elif game == genshin.Game.STARRAIL:
    return (
      "Honkai: Star Rail",
      "https://hyl-static-res-prod.hoyolab.com/communityweb/business/starrail_hoyoverse.png"
    )
  elif game == genshin.Game.GENSHIN:
    return (
      "Genshin Impact",
      "https://fastcdn.hoyoverse.com/static-resource-v2/2023/11/08/9db76fb146f82c045bc276956f86e047_6878380451593228482.png"
    )
  elif game == genshin.Game.ZZZ:
    return (
      "Zenless Zone Zero",
      "https://hyl-static-res-prod.hoyolab.com/communityweb/business/nap.png"
    )

asyncio.run(main())
