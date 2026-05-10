from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import datetime

BOT_TOKEN = '' #Token removed during commit for security
CHANNEL_ID = 1503112069900144862
STUDY_SESSION_TIME_MINUTES = 25
SHORT_BREAK_TIME_MINUTES = 5
LONG_BREAK_TIME_MINUTES = 10


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@tasks.loop(minutes=STUDY_SESSION_TIME_MINUTES, count=4)
async def shortbreak_reminder():
    if shortbreak_reminder.current_loop == 0:
        return
    channel = bot.get_channel(CHANNEL_ID)
    if shortbreak_reminder.current_loop % 4 != 0:
        await channel.send(f"**Take a short {SHORT_BREAK_TIME_MINUTES} minute break!** You have been studying for {STUDY_SESSION_TIME_MINUTES * shortbreak_reminder.current_loop} minutes.")

@tasks.loop(minutes=((STUDY_SESSION_TIME_MINUTES * 4) + (SHORT_BREAK_TIME_MINUTES * 3)), count=2)
async def longbreak_reminder():
    if longbreak_reminder.current_loop == 0:
        return
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a long {LONG_BREAK_TIME_MINUTES} minute break!** You have been studying for {STUDY_SESSION_TIME_MINUTES * shortbreak_reminder.current_loop} minutes.")

@bot.event
async def on_ready():
    print("Hello! Study bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Study bot is ready!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def add(ctx, x, y):
    addresult = int(x) + int(y)
    await ctx.send(f"Result: {addresult}")

@bot.command()
async def mult(ctx, x, y):
    multresult = int(x) * int(y)
    await ctx.send(f"Result: {multresult}")

@bot.command()
async def sub(ctx, x, y):
    subresult = int(x) - int(y)
    await ctx.send(f"Result: {subresult}")

@bot.command()
async def div(ctx, x, y):
    divresult = int(x) / int(y)
    await ctx.send(f"Result: {divresult}")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    shortbreak_reminder.start()
    longbreak_reminder.start()
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
    shortbreak_reminder.stop()
    longbreak_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration}.")

bot.run(BOT_TOKEN)