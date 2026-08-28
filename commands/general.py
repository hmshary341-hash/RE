import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='ping', description='يقيس سرعة استجابة البوت')
  async def ping(self, interaction: discord.Interaction):
    latency = round(self.bot.latency * 1000)
    await interaction.response.send_message(
        f'Pong! 🏓 ({latency}ms)', ephemeral=True
    )


async def setup(bot):
  await bot.add_cog(General(bot))

