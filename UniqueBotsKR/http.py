import aiohttp
import asyncio
import logging

import json

from .errors import UniqueBotsException, HTTPException, Forbidden, NotFound, AuthorizeError
from .model import Hearts, Bot, Categories

baseURL = "https://uniquebots.kr/graphql"
log = logging.getLogger(__name__)

def getGraphQL(query: dict, variables: dict = None):
    if variables is not None:
        return json.dumps({
            "query": query,
            "variables": variables
        }, indent=4)
    else:
        return json.dumps({
            "query": query
        }, indent=4)

async def content_type(response):
    if response.headers['Content-Type'] == 'application/json; charset=utf-8':
        return await response.json()
    return await response.text()

class httpClient:
    """UniqueBots의 Http 클라이언트를 반환합니다.
        이 클래스를 통하여 UniqueBots API에 연결됩니다.
        일부 옵션은 Client를 통하여 전달될 수 있습니다.

        Parameters
        ==========
        **loop: Optional[asyncio.AbstractEventLoop]
            비동기를 사용하기 위한 asyncio.AbstractEventLoop입니다.
            기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.

        **token: Optional[dict]
            UniqueBots의 토큰 값이 들어갑니다.
    """
    def __init__(self, token=None, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()):
        self.loop = loop
        self.token = token
        if token is None:
            self.is_token = False
        else:
            self.is_token = True

    async def requests(self, method: str = "POST", authorize: bool = True, **kwargs):
        """주어진 값에 따른 base를 기반으로 한 API로 보냅니다.

            Parameters
            ==========
            method: Optional[str]
                HTTP 리퀘스트 메소드
                UniqueBots API 특성상, 기본값은 POST로 설정되어 있습니다.
            authorize: Optional[bool]
                API 리퀘스트에 토큰과 함께 전송할지 입니다.
                기본값은 True입니다.

            Raises
            ==========
            .errors.AuthorizeError
                토큰이 필요한 쿼리지만, 클라이언트에 토큰이 주어지지 않았습니다.
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        url = baseURL
        headers = {
            'Content-Type': 'application/json'
        }
        log.debug(f"{url}를 향한 요청이 들어왔습니다.")
        if not self.is_token:
            if authorize:
                raise AuthorizeError("해당 함수는 토큰값이 필요합니다.")
        else:
                headers['Authorization'] = f'Bot {self.token}'
        kwargs['headers'] = headers
        log.debug(f"{url}를 향한 요청이 들어왔습니다.")
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as resp:
                data = await content_type(resp)
                if resp.status == 200:
                    return data
                if resp.status == 400:
                    raise HTTPException(resp, data)
                elif resp.status == 403:
                    raise Forbidden(resp, data)
                elif resp.status == 404:
                    raise NotFound(resp, data)
                else:
                    raise HTTPException(resp, data)
        return

    async def postGuildCount(self, guild_count: int):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            임의적으로 정해진 수치값을 통하여 UniqueBots에 보냅니다.
            본 함수는 토큰이 필요한 기능입니다. 토큰을 넣어주세요.

            Parameters
            ==========
            guild_count: [int]
                서버가 들어가있는 갯수의 값을 지정할 수 있습니다.

            Raises
            ==========
            .errors.AuthorizeError
                토큰이 필요한 쿼리지만, 클라이언트에 토큰이 주어지지 않았습니다.
            .errors.Forbidden
                접근 권한이 없습니다.
            .errors.NotFound
                찾을 수 없습니다, 파라미터를 확인하세요.
            .errors.HTTPException
                알수없는 HTTP 에러가 발생했습니다, 주로 400에 발생합니다.
        """
        payload = getGraphQL(
            query="""
                query($guild_count: Int) {
                    bot(id: "me") {
                        guilds(patch:$guild_count)
                    }
                }
            """, variables=json.dumps({"guild_count": guild_count})
        )
        await self.requests("POST", data=payload)
        return

    async def getHeart(self, bot_id=None):
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
        if bot_id == None:
            if self.is_token:
                bot_id = "me"
            else:
                raise UniqueBotsException("값을 넣어주거나, client를 이용해주세요.")
        payload = getGraphQL(
            query="""
                query($bot_id: String!) {
                    bot (id: $bot_id) { 
                        hearts { from { tag, id, avatarURL } }
                    }
                }
        """, variables=json.dumps({"bot_id": str(bot_id)}))
        data = await self.requests("POST", data=payload, authorize=False)
        return [Hearts(_) for _ in data['data']['bot']['hearts']]

    async def getBot(self, bot_id=None):
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
        if bot_id == None:
            if self.is_token:
                bot_id = "me"
            else:
                raise UniqueBotsException("값을 넣어주거나, client를 이용해주세요.")
        payload = getGraphQL(
            query="""
                query ($bot_id: String!){
                    bot (id: $bot_id) { 
                        id, name, avatarURL, trusted, discordVerified, guilds, status, brief,
                        description, invite, website, support, prefix, library { name }, categories { name, id }
                        hearts { from { tag, id, avatarURL } } 
                    }
                }
        """, variables=json.dumps({"bot_id": str(bot_id)}))
        r_data = await self.requests("POST", data=payload, authorize=False)
        data = r_data['data']['bot']
        data['library'] = data['library']['name']
        data['categories'] = [Categories(_) for _ in data['categories']]
        data['hearts'] = [Hearts(_) for _ in data['hearts']]

        return Bot(data)

    async def getBots(self):
        """본 함수는 코루틴(비동기)를 기반으로 돌아갑니다.
            디스코드 봇 목록을 가져옵니다.

            Returns
            =======
            Value: list
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
        payload = getGraphQL(
            query="""
                query {
                    bots { 
                        id, name, avatarURL, trusted, discordVerified, guilds, status, brief,
                        description, invite, website, support, prefix, library { name }, categories { name, id }
                        hearts { from { tag, id, avatarURL } } 
                    }
                }
        """)
        r_data = await self.requests("POST", data=payload, authorize=False)
        data = r_data['data']['bots']
        f_data = []
        for i in data:
            i['library'] = i['library']['name']
            i['categories'] = [Categories(_) for _ in i['categories']]
            i['hearts'] = [Hearts(_) for _ in i['hearts']]
            f_data.append(i)

        return [Bot(_) for _ in f_data]