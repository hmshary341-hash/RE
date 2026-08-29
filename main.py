import asyncio
import os
import threading
from discord.ext import commands
import discord
from flask import Flas

app = Flask('')

@app.route('/')
def home():
    return 'Bot is running!'

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

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
    # تم تغيير اسم المجلد من commands إلى cogs لعدم التعارض مع مكتبة ديسكورد
    if os.path.exists('./cogs'):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cog_name = filename[:-3]
                await bot.load_extension(f'cogs.{cog_name}')
                print(f'تم تحميل الملف الفرعي: {cog_name}')
    else:
        print("مجلد cogs غير موجود حالياً، يرجى إنشاؤه لإضافة الملفات.")

async def main():
    async with bot:
        threading.Thread(target=run_flask, daemon=True).start()
        await load_cogs()
        await bot.start(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
    asyncio.run(main())
