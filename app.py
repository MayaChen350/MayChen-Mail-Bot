# base files
import discord
from discord.ext import commands
import settings
# from utils import *

#features
from features.post import *
from features.postUpgraded import *

def run():
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

################################
# BASE                        
################################
    @bot.event
    async def on_ready(): 
        await bot.wait_until_ready()
        await bot.tree.sync()
        print("Bot is ready.")

    @bot.event
    async def on_command_error(ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Parameters are missing.")
        else:
            await ctx.send(error)
################################
# Commands
################################             
    bot.add_command(write)
    bot.add_command(send)
    bot.add_command(send_second_version)
   # bot.add_command(check_mayssages)
################################
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

################################

if __name__ == "__main__":
    run()
