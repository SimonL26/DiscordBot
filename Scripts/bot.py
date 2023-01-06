import discord
from discord.ext import commands
import os
import asyncio
import json

# inviteLink = https://discord.com/api/oauth2/authorize?client_id=1054481893044785162&permissions=3298065120321&scope=bot

token_file = open("token.json")
token = json.load(token_file)

description ="""A personal bot that is currently under development."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, description=description)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(token=token['token'])

asyncio.run(main())
# bot.run(TOKEN)

