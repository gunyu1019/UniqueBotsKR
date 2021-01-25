import asyncio
import logging

log = logging.getLogger(__name__)
from .http import httpClient

class client:
    """discord.py Client를 기반으로 한 UniqueBots 클라이언트에 반환합니다.
        이 클래스를 통하여 UniqueBots에게 연결됩니다.
        일부 옵션은 Client를 통하여 전달될 수 있습니다.

        Parameters
        ==========
        bot:
            discord.py의 client() 혹은 bot() 형태의 변수가 들어갑니다.
        **loop: Optional[asyncio.AbstractEventLoop]
            비동기를 사용하기 위한 asyncio.AbstractEventLoop입니다.
            기본값은 None이거나 bot 오브젝트가 들어왔을 때에는 bot.loop입니다.
            기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.
        **autopost: Optional[bool]
            자동으로 1800초(30분)마다 길드 정보를 등록된 토큰값을 통하여 전송할지 설정합니다. 기본값은 False입니다.
    """

    def __init__(self, bot, token: str = None, loop: asyncio.AbstractEventLoop = None, autopost: bool = True):
        self.bot = bot
        self.token = token
        self.loop = loop or bot.loop
        self.http = httpClient(token=self.token, loop=self.loop)
        if autopost:
            self.loop.create_task(self.autopost())

    async def autopost(self, time: int = 30):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            discord.Client의 .guilds의 수를 등록된 토큰을 `postGuildCount()` 통하여 자동으로 UniqueBots에 보냅니다.
            본 함수는 토큰이 필요한 기능입니다. 토큰을 넣어주세요.

            Parameters
            ==========
            ** time: Optional[int]
                시간을 분 단위로 설정합니다. 기본값은 30분입니다.

            Raises
            ==========
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        time = time * 60
        self.time = time

        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            log.info('UniqueBots에 서버 갯수를 자동으로 포스트하고 있습니다.')
            await self.postGuildCount()
            await asyncio.sleep(time)

    def GuildCount(self):
        return len(self.bot.guilds)

    async def postGuildCount(self, guild_count=None):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            discord.Client의 .guild_count의 수를 등록된 토큰을 통하여 UniqueBots에 보냅니다.
            본 함수는 토큰이 필요한 기능입니다. 토큰을 넣어주세요.

            Parameters
            ==========
            ** guild_count: Optional[int]
                서버가 들어가있는 갯수의 값을 임의적으로 지정할 수 있습니다.
                기본값은 모듈에서 자동적으로 `GuildCount()`를 통해 불러옵니다.

            Raises
            ==========
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        log.debug("서버 포스트 요청이 들어왔습니다.")
        if guild_count is None:
            guild_count = self.GuildCount()
        await self.http.postGuildCount(eguild_count=guild_count)

    async def getHeart(self, bot_id ="me"):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            검색하시는 디스코드 봇의 하트 목록을 리스트로 불러옵니다.

            Parameters
            ==========
            ** bot_id: Optional[int]
                하트 목록을 불러올 봇의 ID값이 들어갑니다.
                기본값으로는 CLient를 이용한 `자신의 봇` 값이 들어가게 됩니다.

            Returns
            =======
            Hearts: list
                검색하신 봇에 대한 하트 누른 유저를 리스트로 반환합니다.
                리스트 안에 있는 값은 `Hearts` 형태의 오브젝트로 반환됩니다.

            Raises
            ==========
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        log.debug(f"(ID: {bot_id})의 하트 목록에 대한 요청이 들어왔습니다.")
        return await self.http.getHeart(bot_id)

    async def getHeartUser(self, user_id: int):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            주어진 유저ID의 하트, 투표 유무 정보를 가져옵니다.

            Parameters
            ==========
            user_id: int
                정보를 가져올 유저의 ID값이 들어갑니다.

            Returns
            =======
            Value: bool
                해당 유저가 하트를 눌렀는지의 유/무가 반환됩니다.

            Raises
            ==========
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        log.debug(f"(ID: {user_id})의 하트 유/무 확인에 대한 요청이 들어왔습니다.")
        HeartData = await self.getHeart()
        for i in HeartData:
            if user_id == int(i.id):
                return True
        return False

    async def getBot(self, bot_id="me"):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            주어진 봇 ID의 정보를 가져옵니다.

            Parameters
            ==========
            bot_id: Optional[int]
                정보를 가져올 디스코드 봇의 ID값이 들어갑니다.
                기본값으로는 CLient를 이용한 `자신의 봇` 값이 들어가게 됩니다.

            Returns
            =======
            Bot: object
                해당 봇 정보를 반환합니다.

            Raises
            ==========
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        log.debug(f"(ID: {bot_id})에 대한 디스코드봇 검색결과 요청이 들어왔습니다.")
        return await self.http.getBot(bot_id)

    async def getBots(self):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            디스코드 봇 목록을 가져옵니다.

            Returns
            =======
            Bots: list
                UniqueBots에 등재된 봇 목록을 반환합니다.
                목록 안에 있는 값들은 Bot Object 형태로 반환됩니다.

            Raises
            ==========
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        log.debug("디스코드봇 목록 검색결과 요청이 들어왔습니다.")
        return await self.http.getBots()