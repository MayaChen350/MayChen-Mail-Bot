import discord
from discord.ext import commands
from discord.ui import View, Button
import os
import math
import time
from datetime import datetime

class Mayssage_Box_Menu(View):
    def __init__(self, embed, context, mayssage_box_pages, mayssage_box_dir : str):
        super().__init__()
        self.value = None
        self.embed = embed
        self.context = context
        self.mayssage_box_pages = mayssage_box_pages
        self.mayssage_box_dir = mayssage_box_dir
        self.update_button()

    page_index = 0
    def update_button(self):
        self.children[0].disabled = self.page_index == 0
        self.children[1].disabled = self.page_index + 1 == len(self.mayssage_box_pages)

    async def update_embed(self, interaction : discord.Interaction):
        set_mayssage_box_embed(self.embed, self.context, self.mayssage_box_pages, self.mayssage_box_dir, self.page_index)
        orig_footer = self.embed.footer.text
        self.embed.set_footer(text= "Page " + str(self.page_index + 1) + "/" + str(len(self.mayssage_box_pages)) + "\n" + orig_footer)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(style=discord.ButtonStyle.blurple,label="Prev")
    async def prev(self, interaction : discord.Interaction, button : Button):
        self.page_index -= 1
        self.update_button()
        await self.update_embed(interaction)

    @discord.ui.button(style=discord.ButtonStyle.blurple,label="Next")
    async def next(self, interaction : discord.Interaction, button : Button):
        self.page_index += 1
        self.update_button()
        await self.update_embed(interaction)

class Mayssage_Menu(View):
        def __init__(self, title, messages : list, mayssage_file_name : str):
            super().__init__()
            self.value = None
            self.title = title
            self.messages = messages
            self.mayssage_file_name = mayssage_file_name
            self.update_button()

        page_index = 0
        def update_button(self):
            self.children[0].disabled = self.page_index == 0
            self.children[1].disabled = self.page_index + 1 == len(self.messages)

        async def update_embed(self, interaction : discord.Interaction):
            embed = discord.Embed(title=self.title, description=self.messages[self.page_index])
            embed.clear_fields()
            #embed.add_field(name=self.title, value=self.messages[self.page_index])
            embed.set_footer(text= str(self.page_index + 1) + "/" + str(len(self.messages)))
            await interaction.response.edit_message(embed=embed, view=self)


        @discord.ui.button(style=discord.ButtonStyle.primary,label="Prev")
        async def prev(self, interaction : discord.Interaction, button : Button):
            self.page_index -= 1
            self.update_button()
            await self.update_embed(interaction)

        @discord.ui.button(style=discord.ButtonStyle.primary,label="Next")
        async def next(self, interaction : discord.Interaction, button : Button):
            self.page_index += 1
            self.update_button()
            await self.update_embed(interaction)

        @discord.ui.button(style=discord.ButtonStyle.danger, label="Delete")
        async def delete(self, interaction : discord.Interaction, button : Button):
            view_del = View(timeout=60.0)
            view_del.add_item(Delete_Button(style=discord.ButtonStyle.danger,label="Delete from Maya's computer", mayssage_file_name = self.mayssage_file_name))
            await interaction.response.send_message(content="Are you sure you want to delete this Mayssage?", view=view_del)

class Delete_Button(Button):
    def __init__(self, style, label, mayssage_file_name : str):
        super().__init__()
        self.value= None
        self.style = style
        self.label = label
        self.mayssage_file_name = mayssage_file_name

    async def callback(self, interaction : discord.Interaction):
        os.remove(self.mayssage_file_name)
        await interaction.response.send_message("Mayssage successfully deleted!")

def set_mayssage_box_embed(embed, ctx, mayssage_box_pages, mayssage_box_dir : str, page_index : int):
    embed.timestamp = datetime.fromtimestamp(time.time())
    embed.set_footer(text="MayaChen Mail")
    embed.set_author(name=ctx.author.display_name + "'s Mayssage box")
    embed.clear_fields()

    for mayssageid in mayssage_box_pages[page_index]:
        file = open(mayssage_box_dir + "/" + mayssageid, "r")
        embed.add_field(name=file.readline(), value=(file.readline() + " \- <t:" + file.readline() + ":R>").replace("\n", "")) # In order: Title>
        file.close()

@commands.hybrid_command(description="Check your Mayssages.")
async def check_mayssages(ctx, mayssageid : int = commands.parameter(description="The ID of the Mayssage you want to read")):
    mayssage_box_dir = "data/" + str(ctx.author.id)

    list_dir = os.listdir(mayssage_box_dir)
    list_dir.sort(reverse=True)
    mayssage_box_pages = list()

    for i in range(0, len(list_dir), 3):
        mayssage_box_pages.append(list_dir[i : i + 3])

    mayssage_box_embed = discord.Embed()
    set_mayssage_box_embed(mayssage_box_embed, ctx, mayssage_box_pages,  mayssage_box_dir, 0)
    orig_footer = mayssage_box_embed.footer.text
    mayssage_box_embed.set_footer(text= "Page 1/" + str(len(mayssage_box_pages)) + "\n" + orig_footer)

    mayssage_box_embed_menu = Mayssage_Box_Menu(mayssage_box_embed, ctx, mayssage_box_pages,  mayssage_box_dir)

    #mayssage_box_embed.set_footer(text="MayaChen Mail")
    #mayssage_box_embed.set_author(name=ctx.author.display_name + "'s Mayssage box")

    #for mayssageid in mayssage_box_pages[0]:
     #   file = open(mayssage_box + "/" + mayssageid, "r")
      #  mayssage_box_embed.add_field(name=file.readline(), value=(file.readline() + " \- <t:" + file.readline() + ":R>").replace("\n", "")) # In order: Title, author, relative date
       # file.close()

    mayssage_file_name = "data/" + str(ctx.author.id) + "/" + str(mayssageid)
    mayssage_file = open(mayssage_file_name, "r")
    title = mayssage_file.readline()

    mayssage_content = mayssage_file.read()
    mayssage_file.close()

    mayssage_length = len(mayssage_content)
    mayssage_pages = list()
    mayssage_index = 0

    while mayssage_length > 1000:
        mayssage_pages.append(mayssage_content[mayssage_index:mayssage_index + 1000])
        mayssage_index += 1000
        mayssage_length -= 1000

    mayssage_pages.append(mayssage_content[mayssage_index:-1])

    #embed = discord.Embed(title=title, description = mayssage_pages[0])
    ##embed.add_field(name=title, value=mayssage_pages[0])
    #embed.set_footer(text= "1/" + str(len(mayssage_pages)))
    embed_menu = Mayssage_Menu(title, mayssage_pages, mayssage_file_name)
    await ctx.send(embed=mayssage_box_embed,view=mayssage_box_embed_menu)
