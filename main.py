import os
os.system("pip install -r requirements.txt")
import aiohttp
import asyncio
import tasksio
from colorama import Fore, Style
import random
from dateutil import parser
import datetime
import requests
import sys
import pyfiglet
def clear():
  os.system("clear||cls")


def title(t):
  os.system(f"title {t}")


class colors:
  def ask(qus):
    print(f"{Fore.LIGHTMAGENTA_EX}[?]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

  def what(txt):
    print(f"{Fore.LIGHTBLUE_EX}[?]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def banner(txt):
    print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{txt}{Fore.RESET}{Style.NORMAL}")

  def error(txt):
    print(f"{Fore.RED}[{random.choice(['-', '!'])}]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

  def sucess(txt):
    print(f"{Fore.GREEN}[+]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def warning(txt):
    print(f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

  def log(txt):
    print(f"{Fore.LIGHTMAGENTA_EX}[!]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def msg(txt, idx):
    return f"{Fore.LIGHTBLUE_EX}[{idx+1}]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}"
    
  def ask2(qus):
    print(f"{Fore.LIGHTMAGENTA_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

  def ask3(qus):
    print(f"{Fore.LIGHTBlUE_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")


clear()
title("Promotion Checker - Made By Auth#1337 | .gg/lgnop")

bnr = pyfiglet.figlet_format("LGN")

colors.banner(bnr+"\n")
colors.warning("Made By Auth#1337\n")
colors.ask("Delay: ")
delay = int(input())
colors.ask("Discord User Account Token (required to bypass rate limit): ")
token = input()
auth = {"Authorization": token}
r = requests.get("https://ptb.discord.com/api/v10/users/@me", headers=auth)
if r.status_code in [201,204,200]:
  pass
else:
  colors.error("Invalid Token.")
  sys.exit()


def save(file, data):
  with open(file, "a+") as f:
    f.write(data+"\n")

async def check(promocode):
  async with aiohttp.ClientSession(headers=auth) as cs:
    async with cs.get(f"https://ptb.discord.com/api/v10/entitlements/gift-codes/{promocode}") as rs:
      if rs.status in [200,204,201]:
        data = await rs.json()
        if data["uses"] == data["max_uses"]:
          colors.warning(f"Already Claimed -> {promocode}")
          save("claimed.txt", f"https://discord.com/billing/promotions/{promocode}")
        else:
          try:
            now = datetime.datetime.utcnow()
            exp_at = data["expires_at"].split(".")[0]
            parsed = parser.parse(exp_at)
            days = abs((now-parsed).days)
            title = data["promotion"]["inbound_header_text"]
          except Exception as e:
            print(e)
            exp_at = "Failed To Fetch!"
            days = "Failed To Parse!"
            title = "Failed To Fetch!"
          colors.sucess(f"Valid -> {promocode} | Days Left: {days} | Expires At: {exp_at} | Title: {title}")
          save("valid.txt", f"https://discord.com/billing/promotions/{promocode}")
      elif rs.status == 429:
        try:
          deta = await rs.json()
        except:
          colors.warning("IP Banned.")
          return
        timetosleep = deta["retry_after"]
        colors.warning(f"Rate Limited For {timetosleep} Seconds!")
        await asyncio.sleep(timetosleep)
        await check(promocode)
      else:
        colors.error(f"Invalid Code -> {promocode}")
          
  


async def start():
  codes = open("promotions.txt", "r").read().split("\n")
  try:
    codes.remove("")
  except:
    pass
  async with tasksio.TaskPool(workers=10_000) as pool:
    for promo in codes:
      code = promo.replace('https://discord.com/billing/promotions/', '').replace('https://promos.discord.gg/', '').replace('/', '')
      await pool.put(check(code))
      await asyncio.sleep(delay)


if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  loop.run_until_complete(start())
