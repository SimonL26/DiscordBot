import discord
from discord.ext import commands
import responses
import random 


# async method to send message
async def send_message(message, user_message, is_private:bool):
    try:
        response = responses.handle_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
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

    @bot.command()
    async def add(ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left+right)

    @bot.command()
    async def roll(ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except: 
            await ctx.send("Format has to be in NdN!")
            return 

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.send(result)

    @bot.command(description='For when you wanna settle the score some other way')
    async def choose(ctx, *choices: str):
        await ctx.send(random.choice(choices))

    @bot.command()
    async def repeat(ctx, times: int, content="repeating..."):
        """Repeats a message multiple times"""
        for i in range(times):
            await ctx.send(content)

    @bot.command()
    async def joined(ctx, member: discord.Member):
        await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

    @bot.group()
    async def cool(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

    @cool.command(name="bot")
    async def _bot(ctx):
        await ctx.send("Yes, the bot is cool")

    bot.run(TOKEN)

