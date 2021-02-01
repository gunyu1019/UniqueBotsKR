import discord
import UniqueBotsKR

client = discord.Client()
Bot = UniqueBotsKR.client(client, token='UniqueBots 봇 토큰')

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')

@client.event
async def on_message(message):
    author = message.author
    print(f"{author}투표 유무: {await Bot.getHeartUser(author.id)}")
    # Bool 형태이므로, 두 값에는 True 혹은 False가 리턴됨.

client.run('Discord 토큰')
