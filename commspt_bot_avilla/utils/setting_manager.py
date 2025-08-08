import ssl
from pathlib import Path

import httpx
import yaml
from pydantic import BaseModel

VERIFY_CONTENT = httpx.create_ssl_context(verify=ssl.create_default_context(), http2=True)
CONFIG_FILE = Path.cwd() / ".config.yaml"


class DefinedQQ(BaseModel):
    forward_bot: int
    littleskin_main: int
    littleskin_cafe: int
    commspt_group: int
    csl_group: int
    notification_channel: int
    dev_group: int


class Connection(BaseModel):
    endpoint: str
    access_token: str


class API_SkinRenderMC(BaseModel):
    endpoint: str


class API_mihari_svg(BaseModel):
    endpoint: str


class DB_mongo(BaseModel):
    url: str


class API_bingling_ipip(BaseModel):
    endpoint: str


class API_browserless(BaseModel):
    endpoint: str


class API_littleskin_origin(BaseModel):
    endpoint: str


class API_cloudconfig(BaseModel):
    endpoint: str
    username: str
    password: str


class Setting(BaseModel):
    command_prompt: str = "&"
    defined_qq: DefinedQQ
    connection: Connection
    api_skinrendermc: API_SkinRenderMC
    api_mihari_svg: API_mihari_svg
    db_mongo: DB_mongo
    api_bingling_ipip: API_bingling_ipip
    api_browserless: API_browserless
    api_littleskin_origin: API_littleskin_origin
    api_cloudconfig: API_cloudconfig

    dev_mode: bool
    admin_list: list[int]
    littleskin_admin_token: str


S_ = Setting(**yaml.safe_load(CONFIG_FILE.read_text()))
