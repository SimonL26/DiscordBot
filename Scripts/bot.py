import discord
import responses

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
    TOKEN = "MTA1NDQzODExNzI5OTQ2MjIxNA.GE8fMw.mgZnvuu7nLKmQ5sV_zE5TRlUwNi7F2p-0qmJCo"
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is no running!')

    client.run(TOKEN)
