import discord
from discord.ext import commands

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='command_help')
    async def help(self, context):
        try: 
            await context.send(f"Here are my commands:\n" 
                            "**add_flashcard_set** - Create a new flashcard set or add some to an existing set\n" 
                            "**view_flashcard_sets** - View all of the flashcard sets created\n "
                            "**view_flashcard_set** - View the flashcards in a certain set")
        except Exception as err:
            await context.send(f"Error Occurred: {err}")
    
async def setup(bot):
    await bot.add_cog(Responses(bot))