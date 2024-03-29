from pydantic import BaseModel

import yaml

class DefinedQQ(BaseModel):
    forward_bot: int
    littleskin_main: int
    littleskin_cafe: int
    commspt_group: int
    csl_group: int
    notification_channel: int
    dev_group: int


class Connection(BaseModel):
    qq: int
    host: str
    port: int
    access_token: str


class API_SkinRenderMC(BaseModel):
    endpoint: str


class API_mihari_svg(BaseModel):
    endpoint: str


class DB_mongo(BaseModel):
    url: str


class Setting(BaseModel):
    command_prompt: str = "&"
    defined_qq: DefinedQQ
    connection: Connection
    api_skinrendermc: API_SkinRenderMC
    api_mihari_svg: API_mihari_svg
    db_mongo: DB_mongo

    dev_mode: bool
    admin_list: list[int]
    littleskin_admin_token: str


S_ = Setting(**yaml.load(open(".config.yaml", "r"), Loader=yaml.CBaseLoader))
