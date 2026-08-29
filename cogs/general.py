import discord
from discord.ext import command

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="فحص سرعة استجابة البوت")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! 🏓 البوت شغال بنجاح.")

async def setup(bot):
    await bot.add_cog(General(bot))

