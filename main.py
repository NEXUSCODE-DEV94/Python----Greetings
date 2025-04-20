import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio
import time

load_dotenv()
TOKEN = os.getenv('bot_token')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

greeting_times = {}
last_message_times = {}
message_count = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    current_time = time.time()
    user_id = message.author.id

    if user_id not in last_message_times:
        last_message_times[user_id] = current_time
        message_count[user_id] = 0

    if current_time - last_message_times[user_id] < 2 and message_count[user_id] >= 3:
        await message.author.timeout(duration=10)
        return

    if current_time - last_message_times[user_id] < 2:
        message_count[user_id] += 1
    else:
        message_count[user_id] = 1

    last_message_times[user_id] = current_time

    if 'おはよう' in message.content:
        await message.reply("おはようございます☀️", mention_author=False)

    elif 'こんばんは' in message.content:
        await message.reply("こんばんは🌙", mention_author=False)

    elif 'こんにちは' in message.content:
        await message.reply("こんにちは👋", mention_author=False)

    if user_id not in greeting_times:
        greeting_times[user_id] = 1

    if greeting_times[user_id] == 1:
        greeting_times[user_id] = 2
    elif greeting_times[user_id] == 2:
        greeting_times[user_id] = 3

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Botにログインできました：{bot.user}')

bot.run(TOKEN)
