from datetime import timedelta
import discord
from discord import app_commands
from discord.ext import commands

# 📌 الآدي الخاص بك لتلقي السجلات في الخاص
LOG_RECEIVER_ID = 1495450684731162664

# آديات الرتب المصرح لها باستخدام الأوامر
ALLOWED_ROLE_IDS = [
    1541203322537517127,  # الأونر 1
    1541203661970079885,  # الأونر 2
    1541204029978185838,  # النائب 1
    1541204369339584563,  # النائب 2
    1541204686432895016,  # اليدر 1
    1541205074708275201,  # اليدر 2
    1541205268090589395,  # الادمن 1
    1541206616073043988,  # الادمن 2
]

# آديات رتب التحذيرات والسجن
WARN_1_ID = 1541210101153534032
WARN_2_ID = 1541210228794859632
WARN_3_ID = 1541210359258419333
JAIL_ROLE_ID = 1542872515804799106


def has_allowed_role():
  async def predicate(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
      return True
    user_role_ids = [role.id for role in interaction.user.roles]
    return any(role_id in ALLOWED_ROLE_IDS for role_id in user_role_ids)

  return app_commands.check(predicate)


class Moderation(commands.Cog):

  # تجميع الأوامر تحت مجموعة رئيسية واحدة باسم /admin
  admin = app_commands.Group(
      name='admin', description='لوحة الأوامر الإدارية'
  )

  def __init__(self, bot):
    self.bot = bot

  async def send_private_log(self, bot, embed: discord.Embed):
    try:
      user = await bot.fetch_user(LOG_RECEIVER_ID)
      if user:
        await user.send(embed=embed)
    except:
      pass

  # 1. أمر الحظر (/admin ban)
  @admin.command(name='ban', description='حظر عضو من السيرفر نهائياً')
  @has_allowed_role()
  @app_commands.describe(
      member='العضو المراد حظره', reason='سبب الحظر'
  )
  async def ban(
      self,
      interaction: discord.Interaction,
      member: discord.Member,
      reason: str = 'لم يتم ذكر السبب',
  ):
    await interaction.response.defer()
    await member.ban(reason=reason)
    try:
      dm_embed = discord.Embed(
          title='تم حذرك من السيرفر 🔨',
          description=(
              f'**المسؤول:** {interaction.user.mention}\n**السبب:** {reason}'
          ),
          color=discord.Color.red(),
      )
      await member.send(embed=dm_embed)
    except:
      pass

    log_embed = discord.Embed(
        title='📝 سجل إجراء: [BAN]',
        description=(
            f'**السيرفر:** {interaction.guild.name}\n**المسؤول:**'
            f' {interaction.user.mention}\n**العضو المحظور:**'
            f' {member.mention}\n**السبب:** {reason}'
        ),
        color=discord.Color.red(),
    )
    await self.send_private_log(self.bot, log_embed)

    embed = discord.Embed(
        title='تم الحظر بنجاح 🔨',
        description=(
            f'تم حظر العضو {member.mention}\n**المسؤول:**'
            f' {interaction.user.mention}\n**السبب:** {reason}'
        ),
        color=discord.Color.red(),
    )
    await interaction.followup.send(embed=embed)

  # 2. أمر الطرد (/admin kick)
  @admin.command(name='kick', description='طرد عضو من السيرفر')
  @has_allowed_role()
  @app_commands.describe(
      member='العضو المراد طرده', reason='سبب الطرد'
  )
  async def kick(
      self,
      interaction: discord.Interaction,
      member: discord.Member,
      reason: str = 'لم يتم ذكر السبب',
  ):
    await interaction.response.defer()
    await member.kick(reason=reason)
    try:
      dm_embed = discord.Embed(
          title='تم طردك من السيرفر 👢',
          description=(
              f'**المسؤول:** {interaction.user.mention}\n**السبب:** {reason}'
          ),
          color=discord.Color.orange(),
      )
      await member.send(embed=dm_embed)
    except:
      pass

    log_embed = discord.Embed(
        title='📝 سجل إجراء: [KICK]',
        description=(
            f'**السيرفر:** {interaction.guild.name}\n**المسؤول:**'
            f' {interaction.user.mention}\n**العضو المطرود:**'
            f' {member.mention}\n**السبب:** {reason}'
        ),
        color=discord.Color.orange(),
    )
    await self.send_private_log(self.bot, log_embed)

    embed = discord.Embed(
        title='تم الطرد بنجاح 👢',
        description=(
            f'تم طرد العضو {member.mention}\n**المسؤول:**'
            f' {interaction.user.mention}\n**السبب:** {reason}'
        ),
        color=discord.Color.orange(),
    )
    await interaction.followup.send(embed=embed)

  # 3. أمر الإسكات المؤقت (/admin timeout)
  @admin.command(name='timeout', description='إسكات عضو لفترة محددة')
  @has_allowed_role()
  @app_commands.describe(
      member='العضو المراد إسكافه',
      minutes='المدة بالدقائق',
      reason='سبب الإسكات',
  )
  async def timeout(
      self,
      interaction: discord.Interaction,
      member: discord.Member,
      minutes: int,
      reason: str = 'لم يتم ذكر السبب',
  ):
    await interaction.response.defer()
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    try:
      dm_embed = discord.Embed(
          title='تم إسكاتك مؤقتاً 🔇',
          description=(
              f'**المسؤول:** {interaction.user.mention}\n**المدة:** {minutes}'
              f' دقيقة\n**السبب:** {reason}'
          ),
          color=discord.Color.gold(),
      )
      await member.send(embed=dm_embed)
    except:
      pass

    log_embed = discord.Embed(
        title='📝 سجل إجراء: [TIMEOUT]',
        description=(
            f'**السيرفر:** {interaction.guild.name}\n**المسؤول:**'
            f' {interaction.user.mention}\n**العضو المُسكت:**'
            f' {member.mention}\n**المدة:** {minutes}'
            f' دقيقة\n**السبب:** {reason}'
        ),
        color=discord.Color.gold(),
    )
    await self.send_private_log(self.bot, log_embed)

    embed = discord.Embed(
        title='تم إسكات العضو 🔇',
        description=(
            f'تم إسكات {member.mention} لمدة {minutes}'
            f' دقائق.\n**المسؤول:** {interaction.user.mention}\n**السبب:**'
            f' {reason}'
        ),
        color=discord.Color.gold(),
    )
    await interaction.followup.send(embed=embed)

  # 4. أمر التحذير (/admin warn)
  @admin.command(
      name='warn', description='تحذير عضو (له 3 تحذيرات بالدور)'
  )
  @has_allowed_role()
  @app_commands.describe(
      member='العضو المراد تحذيره', reason='سبب التحذير'
  )
  async def warn(
      self,
      interaction: discord.Interaction,
      member: discord.Member,
      reason: str,
  ):
    await interaction.response.defer()
    guild = interaction.guild
    r1 = guild.get_role(WARN_1_ID)
    r2 = guild.get_role(WARN_2_ID)
    r3 = guild.get_role(WARN_3_ID)

    if not r1 or not r2 or not r3:
      return await interaction.followup.send(
          'رتب التحذيرات غير موجودة في السيرفر، تأكد من الآديات!', ephemeral=True
      )

    assigned_warn = ''
    if r1 not in member.roles:
      await member.add_roles(r1, reason=reason)
      assigned_warn = 'الأول (1)'
    elif r2 not in member.roles:
      await member.add_roles(r2, reason=reason)
      assigned_warn = 'الثاني (2)'
    elif r3 not in member.roles:
      await member.add_roles(r3, reason=reason)
      assigned_warn = 'الثالث (3)'
    else:
      assigned_warn = 'الحد الأقصى (لديه 3 تحذيرات بالفعل)'

    try:
      dm_embed = discord.Embed(
          title='⚠️ تلقيت تحذيراً جديداً',
          description=(
              f'**التحذير:** {assigned_warn}\n**المسؤول:**'
              f' {interaction.user.mention}\n**السبب:** {reason}'
          ),
          color=discord.Color.yellow(),
      )
      await member.send(embed=dm_embed)
    except:
      pass

    log_embed = discord.Embed(
        title='📝 سجل إجراء: [WARN]',
        description=(
            f'**السيرفر:** {interaction.guild.name}\n**المسؤول:**'
            f' {interaction.user.mention}\n**العضو المحذّر:**'
            f' {member.mention}\n**نوع التحذير:**'
            f' {assigned_warn}\n**السبب:** {reason}'
        ),
        color=discord.Color.yellow(),
    )
    await self.send_private_log(self.bot, log_embed)

    embed = discord.Embed(
        title='⚠️ تم تحذير العضو',
        description=(
            f'تم تحذير {member.mention} (التحذير:'
            f' {assigned_warn})\n**المسؤول:**'
            f' {interaction.user.mention}\n**السبب:** {reason}'
        ),
        color=discord.Color.yellow(),
    )
    await interaction.followup.send(embed=embed)

  # 5. أمر إلغاء التحذير (/admin unwarn) بالدور
  @admin.command(
      name='unwarn', description='إلغاء آخر تحذير عن العضو بالدور'
  )
  @has_allowed_role()
  @app_commands.describe(
      member='العضو المراد إلغاء التحذير عنه', reason='السبب'
  )
  async def unwarn(
      self,
      interaction: discord.Interaction,
      member: discord.Member,
      reason: str = 'لم يتم ذكر السبب',
  ):
    await interaction.response.defer()
    guild = interaction.guild
    r1 = guild.get_role(WARN_1_ID)
    r2 = guild.get_role(WARN_2_ID)
    r3 = guild.get_role(WARN_3_ID)

    removed_warn = ''
    if r3 in member.roles:
      await member.remove_roles(r3, reason=reason)
      removed_warn = 'الثالث (3)'
    elif r2 in member.roles:
      await member.remove_roles(r2, reason=reason)
      removed_warn = 'الثاني (2)'
    elif r1 in member.roles:
      await member.remove_roles(r1, reason=reason)
      removed_warn = 'الأول (1)'
    else:
      return await interaction.followup.send(
          'هذا العضو ليس لديه أي تحذيرات لإلغائها!', ephemeral=True
      )

    try:
      dm_embed = discord.Embed(
          title='✅ تم إلغاء تحذير عنك',
          description=(
              f'**تم إلغاء التحذير:** {removed_warn}\n**المسؤول:**'
              f' {interaction.user.mention}\n**السبب:** {reason}'
          ),
          color=discord.Color.green(),
      )
      await member.send(embed=dm_embed)
    except:
      pass

    log_embed = discord.Embed(
        title='📝 سجل إجراء: [UNWARN]',
        description=(
            f'**السيرفر:** {interaction.guild.name}\n**المسؤول:**'
            f' {interaction.user.mention}\n**العضو:**'
            f' {member.mention}\n**تم إلغاء التحذير:**'
            f' {removed_warn}\n**السبب:** {reason}'
        ),
        color=discord.Color.green(),
    )
    await self.send_private_log(self.bot, log_embed)

    embed = discord.Embed(
        title='✅ تم إلغاء التحذير',
        description=(
            f'تم إلغاء التحذير ({removed_warn}) عن العضو'
            f' {member.mention}\n**المسؤول:**'
            f' {interaction.user.mention}\n**السبب:** {reason}'
        ),
        color=discord.Color.green(),
    )
    await interaction.followup.send(embed=embed)

  # 6. أمر السجن (/admin jail) - إغلاق جميع الرومات
  @admin.command(
      name='jail', description='سجن عضو وإغلاق جميع الرومات في وجهه'
  )
  @has_allowed_role()
  @app_commands.describe(
      member='العضو المراد سجنه', reason='سبب السجن'
  )
  async def jail(
      self,
      interaction: discord.Interaction,
      member: discord.Member,
      reason: str = 'لم يتم ذكر السبب',
  ):
    await interaction.response.defer()
    guild = interaction.guild
    jail_role = guild.get_role(JAIL_ROLE_ID)
    if not jail_role:
      return await interaction.followup.send(
          'رتبة السجن غير موجودة في السيرفر (تأكد من الـ ID)!', ephemeral=True
      )

    try:
      await member.add_roles(jail_role, reason=reason)
      for channel in guild.channels:
        try:
          await channel.set_permissions(jail_role, view_channel=False)
        except:
          pass

      try:
        dm_embed = discord.Embed(
            title='🔒 تم سجنك في السيرفر',
            description=(
                f'**المسؤول:** {interaction.user.mention}\n**السبب:** {reason}'
            ),
            color=discord.Color.dark_gray(),
        )
        await member.send(embed=dm_embed)
      except:
        pass

      log_embed = discord.Embed(
          title='📝 سجل إجراء: [JAIL]',
          description=(
              f'**السيرفر:** {interaction.guild.name}\n**المسؤول:**'
              f' {interaction.user.mention}\n**العضو المسجون:**'
              f' {member.mention}\n**السبب:** {reason}'
          ),
          color=discord.Color.dark_gray(),
      )
      await self.send_private_log(self.bot, log_embed)

      embed = discord.Embed(
          title='🔒 تم سجن العضو',
          description=(
              f'تم سجن العضو {member.mention} وإغلاق جميع الرومات'
              f' في وجهه.\n**المسؤول:** {interaction.user.mention}\n**السبب:**'
              f' {reason}'
          ),
          color=discord.Color.dark_gray(),
      )
      await interaction.followup.send(embed=embed)
    except Exception as e:
      await interaction.followup.send(
          f'حدث خطأ أثناء محاولة سجن العضو: {e}', ephemeral=True
      )

  # 7. أمر الإفراج (/admin unjail) - إعادة فتح الرومات
  @admin.command(
      name='unjail', description='الإفراج عن عضو وإعادة فتح الرومات له'
  )
  @has_allowed_role()
  @app_commands.describe(
      member='العضو المراد الإفراج عنه', reason='السبب'
  )
  async def unjail(
      self,
      interaction: discord.Interaction,
      member: discord.Member,
      reason: str = 'لم يتم ذكر السبب',
  ):
    await interaction.response.defer()
    guild = interaction.guild
    jail_role = guild.get_role(JAIL_ROLE_ID)
    if not jail_role:
      return await interaction.followup.send(
          'رتبة السجن غير موجودة في السيرفر (تأكد من الـ ID)!', ephemeral=True
      )

    try:
      await member.remove_roles(jail_role, reason=reason)
      for channel in guild.channels:
        try:
          await channel.set_permissions(jail_role, overwrite=None)
        except:
          pass

      try:
        dm_embed = discord.Embed(
            title='🔓 تم الإفراج عنك في السيرفر',
            description=(
                f'**المسؤول:** {interaction.user.mention}\n**السبب:** {reason}'
            ),
            color=discord.Color.green(),
        )
        await member.send(embed=dm_embed)
      except:
        pass

      log_embed = discord.Embed(
          title='📝 سجل إجراء: [UNJAIL]',
          description=(
              f'**السيرفر:** {interaction.guild.name}\n**المسؤول:**'
              f' {interaction.user.mention}\n**العضو المُفرج عنه:**'
              f' {member.mention}\n**السبب:** {reason}'
          ),
          color=discord.Color.green(),
      )
      await self.send_private_log(self.bot, log_embed)

      embed = discord.Embed(
          title='🔓 تم الإفراج عن العضو',
          description=(
              f'تم الإفراج عن العضو {member.mention} وإعادة فتح'
              f' الرومات.\n**المسؤول:** {interaction.user.mention}\n**السبب:**'
              f' {reason}'
          ),
          color=discord.Color.green(),
      )
      await interaction.followup.send(embed=embed)
    except Exception as e:
      await interaction.followup.send(
          f'حدث خطأ أثناء محاولة الإفراج عن العضو: {e}', ephemeral=True
      )

  # معالجة الأخطاء (بدون أي decorator خاطئ)
  async def cog_app_command_error(
      self, interaction: discord.Interaction, error: app_commands.AppCommandError
  ):
    if isinstance(error, app_commands.CheckFailure):
      if not interaction.response.is_done():
        await interaction.response.send_message(
            'انت مو مخول لهاذا الأمر', ephemeral=True
        )
      else:
        await interaction.followup.send('انت مو مخول لهاذا الأمر', ephemeral=True)
    else:
      if not interaction.response.is_done():
        await interaction.response.send_message(
            f'حدث خطأ: {error}', ephemeral=True
        )
      else:
        await interaction.followup.send(f'حدث خطأ: {error}', ephemeral=True)


async def setup(bot):
  await bot.add_cog(Moderation(bot))
