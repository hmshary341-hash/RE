import asyncio
import os
import threading
from discord.ext import commands
import discord
from flask import Flask

app = Flask('')


@app.route('/')
def home():
  return 'Bot is running!'


def run_flask():
  app.run(host='0.0.0.0', port=8080)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # مهم جداً لتفاعل أوامر البوص مع رتب الأعضاء

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
  print(f'تم تسجيل الدخول: {bot.user}')
  try:
    synced = await bot.tree.sync()
    print(f'تمت مزامنة {len(synced)} أمر/أوامر.')
  except Exception as e:
    print(f'خطأ أثناء مزامنة الأوامر: {e}')


async def load_cogs():
  for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
      cog_name = filename[:-3]
      await bot.load_extension(f'commands.{cog_name}')
      print(f'تم تحميل الملف الفرعي: {cog_name}')


async def main():
  async with bot:
    threading.Thread(target=run_flask).start()
    await load_cogs()
    await bot.start(os.environ['DISCORD_TOKEN'])


if __name__ == '__main__':
  asyncio.run(main())
