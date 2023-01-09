from config import bot_token
from datetime import datetime, time, timedelta
import discord
from discord.ext import commands, tasks
import asyncio
import api

WHEN = time(18, 00)
now = datetime.now()
AUDIO_FILE = 'audio_teste.mp3'

# client = discord.Client()
client = commands.Bot(command_prefix = "!")
channel = client.get_channel(1009189754761396274)

@client.event 
async def on_ready():
    channel = client.get_channel(1009189754761396274)
    #await channel.send(f"aaaaaaaa")

@client.event
async def on_voice_state_update(member, before, after):
    # Verifique se o membro entrou em um canal de voz
    if before.channel is None and after.channel is not None:
        # Obtenha o canal de voz e conecte-se a ele
        channel = after.channel
        voice = await channel.connect()
        # Reproduza o áudio
        voice.play(discord.FFmpegPCMAudio(AUDIO_FILE))
        while voice.is_playing():
            await asyncio.sleep(1)
        # Desconecte-se do canal de voz
        await voice.disconnect()

@client.command()
async def ping(ctx):
    await ctx.channel.send('Pong! {0}'.format(round(client.latency, 1)))

@client.command()
async def clear_all(ctx):
    await ctx.channel.purge()

@client.command()
async def cryptos(ctx):
    await client.wait_until_ready()
    # channel = client.get_channel(1009189754761396274)
    list_with_prices = []
    api.get_coins(list_with_prices= list_with_prices)
    message = (f' \U0001F911 E vamos de precinhos das principais moedas de hoje! \U0001F911\n'
    f'\t- **Bitcoin** => {list_with_prices[0]}\n'
    f'\t- **Ethereum** => {list_with_prices[1]}\n'
    f'\t- **Litecoin** => {list_with_prices[2]}\n'
    f'\t- **Solana** => {list_with_prices[3]}\n'
    f'\t- **Polkadot** => {list_with_prices[4]}\n'
    f'\t- **Cardano** => {list_with_prices[5]}\n'
    f'\t- **Dogecoin** => {list_with_prices[6]}\n')
    await ctx.channel.send(message)

async def remind():
    await client.wait_until_ready()
    channel = client.get_channel(1009189754761396274)
    list_with_prices = []
    api.get_coins(list_with_prices= list_with_prices)
    message = (f' \U0001F911 Sabemos que **o mercado de cripto não fecha nunca**, mas como são 18h vamos de precinhos das principais moedas de hoje! \U0001F911\n'
    f'\t- **Bitcoin** => {list_with_prices[0]}\n'
    f'\t- **Ethereum** => {list_with_prices[1]}\n'
    f'\t- **Litecoin** => {list_with_prices[2]}\n'
    f'\t- **Solana** => {list_with_prices[3]}\n'
    f'\t- **Polkadot** => {list_with_prices[4]}\n'
    f'\t- **Cardano** => {list_with_prices[5]}\n'
    f'\t- **Dogecoin** => {list_with_prices[6]}\n')
    await channel.send(message)

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


# @tasks.loop(hours = 24.0)
# async def remind():
#     channel = client.get_channel(1009189754761396274)
#     price = api.get_price(api.response)
#     await channel.send(price)

# @remind.before_loop
# async def before():
#     await client.wait_until_ready()

# remind.start()


