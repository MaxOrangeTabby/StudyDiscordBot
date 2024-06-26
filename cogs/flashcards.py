import discord
from discord.ext import commands
 

class Flashcards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot;
        self.flashcards = []

        self.flashcard_sets = {}
        self.flashcard_sets_amt = 0

    @commands.command(name="add_flashcard_set")
    async def add_flashcard_set(self, context): 
        def check(other):
            return other.author == context.author and other.channel == context.channel

        try: 
            await context.send("Would you like to add a new set or edit an existing one?\nType \"NEW\" or \"EDIT\"")  
            set_option =   await self.bot.wait_for('message', check=check, timeout=30.0)

            if(set_option.content != "NEW" and set_option.content != "EDIT"):
                await context.send("Not a valid option! :(")
                return

            await context.send("And how many flashcards would you like to make for this set?")
            amt_flashcards_str = await self.bot.wait_for('message', check=check, timeout=30.0)
            amt_flashcards = int(amt_flashcards_str.content)
        
            new_flashcards = []
            for index in range(amt_flashcards):
                await self.add_flashcard(context, new_flashcards)
            
            if(set_option.content == "NEW"):
                await context.send("What would you like to call this new set?")
                set_name = await self.bot.wait_for('message', check=check, timeout=30.0)
                
                self.flashcard_sets[set_name.content] = new_flashcards
                await context.send("Flashcard set created!")
                self.flashcard_sets_amt += 1
            else:
                await context.send("Which set would you like to add this to?")
                set_name = await self.bot.wait_for('message', check=check, timeout=30.0)

                self.flashcard_sets[set_name.content] = new_flashcards
                await context.send("New Flashcards added!")

        except Exception as err:
            await context.send(f"Error Occurred: {err}")
        

    @commands.command(name="view_flashcard_sets")
    async def view_flashcard_sets(self, context):
        try:
            for key, flashcard_set in self.flashcard_sets.items():
                embedCard = discord.Embed(title = f"Set: {key}")
                await context.send(embed=embedCard)
            await context.send("Would you like to view one of the sets?")
            user_res = await self.bot.wait_for('message', chec=check, timeout=30.0)
        except Exception as err:
            await context.send(f"Error Occurred: {err}")

    async def add_flashcard(self, context, list_flashcard):
        def check(other):
            return other.author == context.author and other.channel == context.channel
        try:
            await context.send("Enter Flashcard Title")
            title = await self.bot.wait_for('message', check=check, timeout=30.0)

            await context.send("Enter Flashcard Body")
            body = await self.bot.wait_for('message', check=check, timeout=30.0)

            list_flashcard.append((title.content, body.content))
            await context.send("New Flashcard Added!")

        except Exception as err:
            await context.send(f"Error Occurred: {err}")


    async def view_all_flashcard(self, context, flashcard_set):
         for title, body in flashcard_set:
            embedCard = discord.Embed(title=title, description = body)
            await context.send(embed=embedCard)


async def setup(bot):
    await bot.add_cog(Flashcards(bot))
