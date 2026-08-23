import os
import threading
from flask import Flask
import discord
from discord.ext import commands

app = Flask('')


@app.route('/')
def home():
  return 'Bot is running!'


def run_flask():
  app.run(host='0.0.0.0', port=8080)


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
  print(f'تم تسجيل الدخول: {bot.user}')


@bot.command()
async def ping(ctx):
  await ctx.send('Pong! 🏓')


if __name__ == '__main__':
  threading.Thread(target=run_flask).start()
  # التوكن سيسحبه تلقائياً من إعدادات المنصة (Environment Variables)
  bot.run(os.environ['DISCORD_TOKEN'])
