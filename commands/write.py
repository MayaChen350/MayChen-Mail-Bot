from discord.ext import commands

@commands.hybrid_command()
async def write(ctx):
    """This command is perfect to start a message\n
    The bot starts recording messages from its last message to the send command"""
    
    await ctx.send(f"Welcome to MayChen Mail! Write all your messages you want to send to your destinataire, and use the `send` command to send all your messages. (The limit of messages is 200)")