from discord.ext import commands
import discord
from dataclasses import dataclass
import datetime

BOT_TOKEN = '' #Removed during commit for secuirty
CHANNEL_ID = 1499594271701995635
MAX_SESSION_TIME_MINUTES = 30

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello! Study bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Study bot is ready!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int()
    await ctx.send(f"Result: {result}")

@bot.command()
async def sub(ctx, x, y):
    result = int(x) - int(y)
    await ctx.send(f"Result: {result}")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    await ctx.send(f"New study session started at {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    await ctx.send(f"Session ended after {human_readable_duration}.")

bot.run(BOT_TOKEN)