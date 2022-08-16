from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    bilibili_cookie: str = "SESSDATA=861ef354%2C1669685313%2Cce247%2A61;"
