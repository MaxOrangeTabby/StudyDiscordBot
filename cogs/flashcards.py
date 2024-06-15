from discord.ext import commands

class Flashcards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot;
        self.flashcards = []

    @commands.command(name='add_flashcard')
    async def add_flashcard(self, context):
        def check(other):
            return other.author == context.author and other.channel == context.channel

        try:
            await context.send("Enter Flashcard Title")
            title = await self.bot.wait_for('message', check=check, timeout=30.0)

            await context.send("Enter Flashcard Body")
            body = await self.bot.wait_for('message', check=check, timeout=30.0)

            self.flashcards.append((title.content, body.content))
            await context.send("New Flashcard Added!")

        except Exception as excep:
            await context.send("Error occurred: {excep}")


    
    @commands.command(name='add_multiple_flashcard')
    async def add_multiple_flashcard(self):
        return