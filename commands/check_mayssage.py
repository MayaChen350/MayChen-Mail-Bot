import discord
from discord.ext import commands
import os

from components import MayssageBoxMenu

@commands.hybrid_command(description="Check your Mayssages.")
async def check_mayssages(ctx):
    mayssage_box_dir = "data/" + str(ctx.author.id)

    list_dir = os.listdir(mayssage_box_dir)
    list_dir.sort(reverse=True)
    mayssage_box_pages = list()

    for i in range(0, len(list_dir), 3):
        mayssage_box_pages.append(list_dir[i : i + 3])

    mayssage_box_embed_menu = MayssageBoxMenu(mayssage_box_embed, ctx)
    mayssage_box_embed = discord.Embed()
    orig_footer = mayssage_box_embed.footer.text
    mayssage_box_embed.set_footer(text= "Page 1/" + str(len(mayssage_box_pages)) + "\n" + orig_footer)

    await ctx.send(embed=mayssage_box_embed,view=mayssage_box_embed_menu)