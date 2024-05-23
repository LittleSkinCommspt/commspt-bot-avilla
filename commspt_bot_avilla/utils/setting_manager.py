import ssl
import httpx
from pydantic import BaseModel

import yaml

VERIFY_CONTENT = httpx.create_ssl_context(verify=ssl.create_default_context(), http2=True)


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


class Feishu_Bitable(BaseModel):
    app_token: str
    table_id: str
    access_token: str


class Setting(BaseModel):
    command_prompt: str = "&"
    defined_qq: DefinedQQ
    connection: Connection
    api_skinrendermc: API_SkinRenderMC
    api_mihari_svg: API_mihari_svg
    db_mongo: DB_mongo
    api_bingling_ipip: API_bingling_ipip
    api_browserless: API_browserless
    # feishu_bitable: Feishu_Bitable

    dev_mode: bool
    admin_list: list[int]
    littleskin_admin_token: str


S_ = Setting(**yaml.load(open(".config.yaml", "r"), Loader=yaml.CBaseLoader))
