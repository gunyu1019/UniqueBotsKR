class UniqueBotsException(Exception):
    """UniqueBotsKr의 기본 예외 클래스입니다."""
    pass


class HTTPException(UniqueBotsException):
    """.HTTPClient의 기본 예외 클래스입니다."""
    def __init__(self, response, message):
        self.response = response
        if isinstance(message, dict):
            self.text = message.get('message','')
            self.code = message.get('code', 0)
        else:
            self.text = message

        if self.text != '':
            super().__init__(f"{response.reason} (상태코드: {response.status}): {self.text}")
        else:
            super().__init__(f"{response.reason} (상태코드: {response.status})")


class AuthorizeError(UniqueBotsException):
    """토큰이 필요한 엔드포인트지만, 클라이언트에 토큰이 주어지지 않았습니다."""
    pass


class Forbidden(HTTPException):
    """접근 권한이 없을 때 발생합니다."""
    pass


class NotFound(HTTPException):
    """해당 항목을 찾을 수 없을 때 발생합니다."""
    pass
