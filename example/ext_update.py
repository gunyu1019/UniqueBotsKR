import UniqueBotsKR
from discord.ext import commands

client = commands.Bot()
Bot = UniqueBotsKR.client(client, token='UniqueBots 봇 토큰',autopost=True)

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')

client.run('Discord 토큰')
