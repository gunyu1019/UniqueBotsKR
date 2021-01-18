class UniqueBotsResponse:
    """.HTTPClient의 모든 반환 데이터에 대한 기본 모델입니다.

        Returns
        =======
        response: dict
            반환되는 데이터의 dict입니다.
        attribute
            attribute의 이름을 입력하면 해당 값을 반환합니다.
    """
    def __init__(self, response):
        self.response = response

    def __getattr__(self, attr):
        return self.response.get(attr)

    def __dict__(self):
        return self.response

class Hearts(UniqueBotsResponse):
    """.HTTPClient의 디스코드 하트 정보 데이터의 모델입니다.

        Returns
        =======
        response: dict
            반환되는 데이터의 dict입니다.
        attribute
            attribute의 이름을 입력하면 해당 값을 반환합니다.
    """
    def __init__(self, response):
        super().__init__(response['from'])

class Bot(UniqueBotsResponse):
    """.HTTPClient의 디스코드 봇 정보 데이터의 모델입니다.

        Returns
        =======
        response: dict
            반환되는 데이터의 dict입니다.
        attribute
            attribute의 이름을 입력하면 해당 값을 반환합니다.
    """
    def __init__(self, response):
        super().__init__(response)

class Categories(UniqueBotsResponse):
    """.HTTPClient의 디스코드 봇 카테고리 데이터의 모델입니다.

        Returns
        =======
        response: dict
            반환되는 데이터의 dict입니다.
        attribute
            attribute의 이름을 입력하면 해당 값을 반환합니다.
    """
    def __init__(self, response):
        super().__init__(response)