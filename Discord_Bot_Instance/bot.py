from discord.ext import commands
import discord
import requests

intents = discord.Intents.default()
intents.typing= True
intents.message_content = True

bot = commands.Bot(command_prefix='..', description='A simple Discord bot that starts game servers', intents=intents)
# Your discord bot token here
token = '[TOKEN]'
# Your cloud functions http trigger URL here
minecraft_url = '[CLOUD_FUNCTIONS_URL]'

def start_server(url):
        response = requests.get(url)
        return response.text

@bot.command(
        help="Starts minecraft server. Takes about 30 - 60 seconds.",
        brief="Starts minecraft server."
)
# My discord command 'trigger' is 'startMinecraft', but simply change the function name to whatever you want the command to be
async def startMinecraft(ctx):
        await ctx.send("Starting Server... Please Wait")
        done = start_server(minecraft_url)
        await ctx.send(done)

bot.run(token)
