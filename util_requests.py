__all__ = (
    'OAuth2',
    'SessionWithUrlPrefix',
    'upload',
)

import os
from typing import TYPE_CHECKING, Optional, Union

from requests.auth import AuthBase
from requests.sessions import Session

if TYPE_CHECKING:
    import io
    from requests import Request, Response


class SessionWithUrlPrefix(Session):
    """可设置前缀的 session.

    >>> s = SessionWithUrlPrefix('http://localhost/api')
    >>> r = s.get('/user')  # r.request.url == 'http://localhost/api/user'
    """

    def __init__(self, prefix: Optional[str] = None):
        super().__init__()
        self.prefix = prefix

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}'
            f' prefix={self.prefix!r}'
            f'>'
        )

    def request(self, method: str, url: str, *args, **kwargs) -> 'Response':
        url = url if self.prefix is None else self.prefix + url
        return super().request(method, url, *args, **kwargs)


class OAuth2(AuthBase):
    """自定义 OAuth2.

    >>> s = Session()
    >>> s.auth = OAuth2('123')
    >>> r = s.get('http://localhost/api/user')
    """

    def __init__(self, token: str):
        self.token = token

    def __call__(self, r: 'Request') -> 'Request':
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


def upload(url: str, file: Union[str, io.StringIO],
           file_name: str = None) -> 'Response':
    """上传文件到某个 url.

    `file`: 可以是一个 str 代表文件路径, 也可以是一个类文件对象, 比如 `io.StringIO`.
    `file_name`: 上传的文件名, 如果指定, 则为此参数.
                 如果不指定此参数且 `file` 类型是 `str`, 那么从 `file` 中提取,
                 如果不指定此参数且 `file` 类型是 `io.StringIO`, 那么为 `data.csv`.
    """
    import requests

    if isinstance(file, str):
        file_name = os.path.split(file)[1] if file_name is None else file_name
        file = open(file)
    else:
        file_name = 'data.csv' if file_name is None else file_name

    r = requests.post(url=url, files={'file': (file_name, file)})
    return r
