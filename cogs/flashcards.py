import discord
from discord.ext import commands
 

class Flashcards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check(self,context, other):
        return other.author == context.author and other.channel == context.channel
    
    # Used to add new flashcards to a set or edit an existing one
    @commands.command(name="add_flashcard_set")
    async def add_flashcard_set(self, context):
        def check_other(other):
            return self.check(context, other)

        try: 
            await context.send("Would you like to add a new set or edit an existing one?\nType \"NEW\" or \"EDIT\"")  
            set_option = await self.bot.wait_for('message', check=check_other, timeout=30.0)
            str_option_str = (set_option.content).lower()

            if(str_option_str != "new" and str_option_str != "edit"):
                await context.send("Not a valid option! :(")
                return

            await context.send("And how many flashcards would you like to make for this set?")
            amt_flashcards_str = await self.bot.wait_for('message', check=check_other, timeout=30.0)
            amt_flashcards = int(amt_flashcards_str.content)
        
            new_flashcards = []
            for index in range(amt_flashcards):
                await self.add_flashcard(context, new_flashcards)
            
            if(str_option_str == "new"):
                await context.send("What would you like to call this new set?")
                set_name = await self.bot.wait_for('message', check=check_other, timeout=30.0)
                
                self.bot.flashcard_sets[set_name.content] = new_flashcards
                await context.send("Flashcard set created!")
                self.bot.flashcard_sets_amt += 1
            else:
                await context.send("Which set would you like to add this to?")
                set_name = await self.bot.wait_for('message', check=check_other, timeout=30.0)

                self.bot.flashcard_sets[set_name.content] = new_flashcards
                await context.send("New Flashcards added!")

        except Exception as err:
            await context.send(f"Error Occurred: {err}")
        
    # View all of the flashcard sets
    @commands.command(name="view_flashcard_sets")
    async def view_flashcard_sets(self, context):
        def check_other(other):
            return self.check(context, other)
        
        try:
            for key, flashcard_set in self.bot.flashcard_sets.items():
                embedCard = discord.Embed(title = f"Set: {key}")
                await context.send(embed=embedCard)
            await context.send("Would you like to view one of the sets?\n Type \"YES\" or \"NO\"")
            user_res = await self.bot.wait_for('message', check=check_other, timeout=30.0)

            if((user_res.content).lower() != "yes" and (user_res.content).lower() != "no"):
                await context.send("Now a valid option! :(")
                return
            
            await   self.view_flashcard_set(context)
            
        except Exception as err:
            await context.send(f"Error Occurred: {err}")

    # View all of the flashcards in a set
    @commands.command(name="view_flashcard_set")
    async def view_flashcard_set(self, context):
        def check_other(other):
            return self.check(context, other)

        try:
            finding_set = True
            while(finding_set):
                await context.send("Which set would you like to view? (Case Matters!)")
                set_name = await self.bot.wait_for('message', check=check_other, timeout=30.0)

                if((set_name.content).lower() == "cancel"):
                    await context.send("Exiting process!")
                    return

                if(set_name.content in self.bot.flashcard_sets):
                    await context.send(f"All flashcards in Set {set_name.content}:")
                    await self.view_all_flashcard(context, self.bot.flashcard_sets[set_name.content])
                    return
                else:
                    await context.send("That set doesn't exist, try again or type \"Cancel\" to exit")
        except Exception as err:
            await context.send(f"Error Occurred: {err}")

    # Helper function to add flashcards to a certain set
    async def add_flashcard(self, context, list_flashcard):
        def check_other(other):
            return self.check(context, other)
        
        try:
            await context.send("Enter Flashcard Title")
            title = await self.bot.wait_for('message', check=check_other, timeout=30.0)

            await context.send("Enter Flashcard Body")
            body = await self.bot.wait_for('message', check=check_other, timeout=30.0)

            list_flashcard.append({title.content, body.content})
            await context.send("New Flashcard Added!")

        except Exception as err:
            await context.send(f"Error Occurred: {err}")


    # Helper function to view all of the flashcards in a set
    async def view_all_flashcard(self, context, flashcard_set):        
        for title, body in flashcard_set:
            embedCard = discord.Embed(title=title, description = body)
            await context.send(embed=embedCard)


async def setup(bot):
    await bot.add_cog(Flashcards(bot))
