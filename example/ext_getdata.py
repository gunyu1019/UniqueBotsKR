import UniqueBotsKR
from discord.ext import commands

client = commands.Bot()
Bot = UniqueBotsKR.client(client, token='UniqueBots 봇 토큰')

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')

@client.command(name='데이터')
async def _update(ctx):
    data = await Bot.getBot(680694763036737536)
    await ctx.send(f"{data}")
    
client.run('Discord 토큰')
