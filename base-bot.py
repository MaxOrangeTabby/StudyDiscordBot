import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Flashcard set structure -> {Set Name, Set List}
# Set List structure -> [{Question, Answer}, {Question, Answer}, {Question, Answer}]
bot.flashcard_sets = {}
bot.flashcard_sets_amt = 0

@bot.command(name='ping')
async def ping(context):
    await context.send('Hop on League')

async def load_cogs():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")
        except Exception as e:
           print({e})
           
@bot.event
async def on_ready():
    await load_cogs()
bot.run(TOKEN)
