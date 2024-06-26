import discord
from discord.ext import commands

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='command_help')
    async def help(self, context):
        return
    
async def setup(bot):
    await bot.add_cog(Responses(bot))