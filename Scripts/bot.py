import discord
from discord.ext import commands
import os
import asyncio

TOKEN = "MTA1NDQ4MTg5MzA0NDc4NTE2Mg.GzRjtC.-F72HmFY81wTT93dOS1VsJypotqxyHOF_jZALs"
description ="""A personal bot that is currently under development."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents, description=description)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print("----------")

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(token=TOKEN)

asyncio.run(main())
# bot.run(TOKEN)

