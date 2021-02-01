#-*- coding: utf-8 -*-
import discord
from discord.ext import commands
import UniqueBotsKR

INTENTS = discord.Intents.default()
INTENTS.members = False
INTENTS.presences = False

bot = commands.Bot(command_prefix='접두사', intents=INTENTS)
TOKEN='토큰'
unitoken='토큰'

@bot.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + bot.user.name)
    print("디스코드봇 ID:" + str(bot.user.id))
    print("디스코드봇 버전:" + str(bot.__version__))
    print('------')

@bot.command(name="유니크봇리스트",aliases=["uniquebotslist"], help="로드을 합니다.")
async def uniquebots_list(ctx):
    status_dict: dict = {'online': '온라인', 'offline': '오프라인','invisible': '오프라인', 'idle': "자리비움",'dnd': "방해금지"}
    Unique=UniqueBotsKR.client(bot,unitoken)
    data= await Unique.getBots()
    n = 1
    rank=[]
    embed = discord.Embed(title="봇하트순위", description ='[홈페이지](https://uniquebots.kr/)')
    for x in data:
        status = status_dict[x.status]
        rank.append([x.name,status,x.guilds,len(x.hearts),x.prefix,x.brief,x.invite])
    rank = list(reversed(sorted(rank, key=lambda x:x[1])))
    for i in rank:
        if n>11:
            break
        embed.add_field(name=f'{n}',value=f' {i[0]} {i[1]}\n{i[2]}서버 ❤️ {i[3]} 접두사:{i[4]}\n짧은설명:{i[5]}\n[초대하기]({i[6]})')
        n += 1
    await ctx.send(embed= embed)
    
bot.run(TOKEN)
