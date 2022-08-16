from config import bot_token
from datetime import datetime, time, timedelta
import discord
from discord.ext import commands, tasks
import asyncio

WHEN = time(17, 42)
print(WHEN)
now = datetime.now()
print(now.time())

client = discord.Client()
channel = client.get_channel(1009189754761396274)

@client.event 
async def on_ready():
    pass

async def remind():
    await client.wait_until_ready()
    channel = client.get_channel(1009189754761396274)
    await channel.send("hellooooo momolado!")

async def background_task():
    now = datetime.now()
    if now.time() == WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.now() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await remind()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)

client.loop.create_task(background_task())
client.run(bot_token)