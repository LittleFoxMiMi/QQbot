from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    bilibili_cookie: str = "SESSDATA=b9f6be9a%2C1676169660%2C4a02c%2A81;"
