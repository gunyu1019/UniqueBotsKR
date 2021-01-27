# UniqueBotsKR
[Uniquebots](https://uniquebots.kr/)를 위한 비공식 파이썬 API 레퍼입니다.

## 목차
* [설치 (Installation)](#설치-Installation)
* [로깅 (Logging)](#로깅-Logging)
* [오브젝트 (Object)](#오브젝트-Object)
  * [Bot](#Bot)
  * [Categories](#Categories)
  * [Hearts](#Hearts)
* [예시(Example)](#예시-Example)
  * [자동으로 서버 수 업데이트하기](#자동으로-서버-수-업데이트하기)
  * [직접 서버 수 업데이트하기](#직접-서버-수-업데이트하기)
  * [유저 하트 유무 불러오기](#유저-하트-유무-불러오기)
  * [봇의 아이디로 봇 정보 불러오기](#봇의-아이디로-봇-정보-불러오기)


## 설치 (Installation)
파이썬 3.6 혹은 그 이상의 버전이 필요합니다.
**Install via pip (recommended)**
```
# Linux/macOS
python -3 -m pip install UniqueBotsKR

# Windows
py -3 -m pip install UniqueBotsKR
```

**Install from source**
```
# Linux/macOS
python -3 -m pip install git+https://github.com/gunyu1019/Unoffical-UniqueBots-py-SDK

# Windows
py -3 -m pip install git+https://github.com/gunyu1019/Unoffical-UniqueBots-py-SDK
```
## 로깅(Logging)
UniqueBotsKR은 파이썬의 `logging` 모듈을 사용하여, 오류 및 디버그 정보를 기록합니다.
로깅 모듈이 설정되지 않은 경우 오류 또는 경고가 출력되지 않으므로 로깅 모듈을 구성하는 것이 좋습니다.

로깅 모듈의 레벨은 `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`가 있으며 `INFO`로 설정하는 것을 추천합니다.
```python
import logging

logger = logging.getLogger("UniqueBotsKR")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(filename)s] [%(name)s:%(module)s] [%(levelname)s]: %(message)s'))
logger.addHandler(handler)
```

## 오브젝트 (Object)
일부 함수는 Object 형태로 반환됩니다. 아래의 목록은 특정 함수를 통해 불러온 값을 통하여 불러올 수 있는 값입니다.

### Bot
Bot 혹은, Bots를 사용했을 때 다음과 같이 값을 불러올 수 있습니다.
* id : 디스코드봇 ID
* name : 디스코드봇 이름
* avatarURL : 디스코드봇 프로필 사진 URL 
* trusted : UniqueBots 인증 유/무
* discordVerified : 디스코드봇 인증 유/무
* guilds : 활동 중인 서버 수(UniqueBots에 등재된 기준)
* status : 상태
* brief : 짧은 소개글
* description : 긴 소개글
* invite : 초대 링크
* website : 웹사이트
* support : 지원 서버 주소
* prefix : 접두어
* library : 사용 중인 디스코드 라이브러리
* categories : 카테고리 목록
* hearts : 하트 목록

### Categories
Bot 오브젝트안에 있는 Categories 목록에 들어있는 값은 다음과 같이 값을 불러올수 있습니다.
* name : 카테고리 이름
* id : 카테고리 ID

### Hearts
Bot 오브젝트안에 있는 Hearts 혹은, Hearts 를 통하여 불러온 목록에 들어있는 값은 다음과 같이 값을 불러올수 있습니다.
* id : 사용자 디스코드 ID
* tag : 사용자 디스코드 태그(ㅇㅇㅇ#1234) 
* avatarURL : 사용자 프로필 사진 URL

## 예시 (Example)
### 자동으로 서버 수 업데이트하기
주기적으로 봇의 수를 업데이트합니다. (discord.Client 기준)
```python
import discord
import UniqueBotsKR

client = discord.Client()
Bot = UniqueBotsKR.client(client, token='UniqueBots 봇 토큰',autopost=True)

@client.event
async def on_ready():
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')

client.run('Discord 토큰')
```

주기적으로 봇의 수를 업데이트합니다. (discord.ext.command 기준)
```python
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
```

### 직접 서버 수 업데이트하기
사용자가 직접 서버 수를 업데이트 할 수 있습니다.
```python
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
    if message.content == "서버수업데이트":
        await Bot.postGuildCount()

client.run('Discord 토큰')
```

### 유저 하트 유무 불러오기
특정 사용자가 하트를 눌렀는지에 대한 유/무 값을 반환합니다.
```python
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
```

### 봇의 아이디로 봇 정보 불러오기
봇ID를 통하여 UniqueBots에 등재된 디스코드봇을 불러올 수 있습니다.
```python
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
    
    data = Bot.getBot(680694763036737536)
    print(f"{data}")
    
client.run('Discord 토큰')
```
