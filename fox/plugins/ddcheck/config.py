from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    bilibili_cookie: str = "SESSDATA=4dc4e6c6%2C1683947081%2Ca1610%2Ab2;"
