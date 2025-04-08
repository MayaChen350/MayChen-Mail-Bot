# base files
from discord.ext import commands
import settings

# commands
from commands.write import write
from commands.send import send
from commands.check_mayssage import check_mayssages
from commands.notification_settings import notification_settings

def run():
    bot : commands.Bot = settings.bot

################################
# BASE                        
################################
    @bot.event
    async def on_ready(): 
        await bot.wait_until_ready()
        await bot.tree.sync()
        print("Bot is ready.")

    @bot.event
    async def on_command_error(ctx,error : commands.CommandError):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Parameters are missing.")
        else:
            await ctx.send(error)
################################
# Commands
################################             
    bot.add_command(write)
    bot.add_command(send)
    bot.add_command(check_mayssages)
    bot.add_command(notification_settings)
################################
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

################################

if __name__ == "__main__":
    run()
