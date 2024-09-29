from discord.ext import commands

from components.UI.MayssageBox import MayssageBox

@commands.hybrid_command(description="Check your Mayssages.")
async def check_mayssages(ctx):
    """Display the Mayssage Box with the Mayssage of the user who sent the commend"""
    mayssage_box = MayssageBox(ctx)
    await ctx.send(embed=mayssage_box.embed,view=mayssage_box)