import discord
import random

from discord.ext import commands

class Flashcards_Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check(self,context, other):
        return other.author == context.author and other.channel == context.channel
    
    @commands.command(name = "flashcard_quiz")
    async def flashcard_quiz(self, context):
        def check_other(other):
            return self.check(context, other)
        
        try:
            set_to_quiz = None
            finding_set = True
            while(finding_set):
                await context.send("Which set would you like to be quizzed on? Case matters!")
                set_name = await self.bot.wait_for('message', check=check_other, timeout=30.0)

                if((set_name.content).lower() == "cancel"):
                    await context.send("Exiting process!")
                    return

                if(set_name.content in self.bot.flashcard_sets):
                    set_to_quiz = self.bot.flashcard_sets[set_name.content]
                    finding_set = False
                else:
                    await context.send("That set doesn't exist, try again or type \"Cancel\" to exit")


            for question, answer in set_to_quiz:
                await context.send(f"What is the answer to: {question}")
                user_res = await self.bot.wait_for('message', check=check_other, timeout=30.0)
                await context.send(f"The answer is: {answer} \n Your answer was: {user_res.content}")

                await context.send("Type \"Next\" for the next question or \"Cancel\" to exit")
                user_res = await self.bot.wait_for('message', check=check_other, timeout=30.0)
                if((user_res.content).lower() == "cancel"):
                    await context.send("Exiting Process")
                    return
        except Exception as err:
            await context.send(f"Error Occurred: {err}")

    @commands.command(name = "flashcard_quiz_shuffle")
    async def flashcard_quiz_shuffle(self, context):
        def check_other(other):
            return self.check(context, other)
        
        try:
            set_to_quiz = None 
            finding_set = True
            while(finding_set):
                await context.send("Which set would you like to be quizzed on? Case matters!")
                set_name = await self.bot.wait_for('message', check=check_other, timeout=30.0)

                if((set_name.content).lower() == "cancel"):
                    await context.send("Exiting process!")
                    return

                if(set_name.content in self.bot.flashcard_sets):
                    set_to_quiz = self.bot.flashcard_sets[set_name.content]
                    finding_set = False
                else:
                    await context.send("That set doesn't exist, try again or type \"Cancel\" to exit")
                
            set_size = len(set_to_quiz)
            visited_num = []
            random_num = random.randint(0,(set_size-1))

            while(len(visited_num) != set_size):
                flashcard = set_to_quiz[random_num]
                title, body = next(iter(flashcard.items()))

                visited_num.append(random_num)
                await context.send(f"What is the answer to: {title}")

                user_res = await self.bot.wait_for('message', check=check_other, timeout=30.0)

                await context.send(f"The answer is: {body} \n Your answer was: {user_res.content}")

                await context.send("Type \"Next\" for the next question or \"Cancel\" to exit")
                user_res = await self.bot.wait_for('message', check=check_other, timeout=30.0)
                if((user_res.content).lower() == "cancel"):
                    await context.send("Exiting Process")
                    return
                
                while(random_num not in visited_num):
                    random_num = random.ranint(0, (set_size-1))
        except Exception as err:
            await context.send(f"Error Occurred: {err}")

async def setup(bot):
    await bot.add_cog(Flashcards_Quiz(bot))