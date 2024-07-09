import discord
from discord.ui import View, Button
from datetime import datetime

from DeleteButton import DeleteButton

class MayssageReadMenu(View):
        def __init__(self, title, mayssage_pages : list, mayssage_file_name : str, author : str, time : datetime):
            super().__init__()
            self.value = None
            self.title = title
            self.mayssage_pages = mayssage_pages
            self.mayssage_file_name = mayssage_file_name
            self.author = author
            self.time = time
            self.update_button()

        page_index = 0
        def update_button(self):
            self.children[0].disabled = self.page_index == 0
            self.children[1].disabled = self.page_index + 1 == len(self.mayssage_pages)

        async def update_embed(self, interaction : discord.Interaction):
            embed = discord.Embed(title=self.title, description=self.mayssage_pages[self.page_index], timestamp=self.time)
            embed.clear_fields()
            embed.set_footer(text= "Page " + str(self.page_index + 1) + "/" + str(len(self.mayssage_pages)) + "\nBy " + self.author)
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
            view_del.add_item(DeleteButton(style=discord.ButtonStyle.danger,label="Delete from Maya's computer", mayssage_file_name = self.mayssage_file_name))
            await interaction.response.send_message(content="Are you sure you want to delete this Mayssage?", view=view_del)
