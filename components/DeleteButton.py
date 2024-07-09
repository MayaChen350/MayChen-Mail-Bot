import discord
from discord.ui import Button
import os

class DeleteButton(Button):
    def __init__(self, style, label, mayssage_file_name : str):
        super().__init__()
        self.value= None
        self.style = style
        self.label = label
        self.mayssage_file_name = mayssage_file_name

    async def callback(self, interaction : discord.Interaction):
        os.remove(self.mayssage_file_name)
        await interaction.response.send_message("Mayssage successfully deleted!")
