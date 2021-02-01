#-*- coding: utf-8 -*-
import discord
from discord.ext import commands

INTENTS = discord.Intents.default()
INTENTS.members = False
INTENTS.presences = False

bot = commands.Bot(command_prefix='접두사', intents=INTENTS)
TOKEN='토큰'

@bot.command(name="로드",aliases=["fhem"], help="로드을 합니다.")
async def load(ctx, extension):
    bot.load_extension(f"Cogs.{extension}")
    await ctx.send(f":white_check_mark: {extension}을(를) 로드했습니다!")

bot.run(TOKEN)
