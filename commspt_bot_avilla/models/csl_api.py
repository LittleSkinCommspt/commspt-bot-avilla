from typing import Literal

import httpx
from pydantic import BaseModel, model_validator
from pydantic.fields import Field
from richuru import logger


class CustomSkinLoaderApi(BaseModel):
    username: str | None
    skins: dict[Literal["default", "slim"], str | None] | None
    skin_hash: str | None = None
    cape_hash: str | None = Field(None, alias="cape")
    player_existed: bool | None = True
    skin_type: Literal["default", "slim"] | None = None
    skin_existed: bool | None = True
    cape_existed: bool | None = True

    @model_validator(mode="before")
    @classmethod
    def pre_processor(cls, values: dict):
        #
        player_existed = bool(values)
        if not player_existed:
            skin_type = None
            skin_existed = False
            cape_existed = False
        else:
            skin_type = "slim" if "slim" in values["skins"] else "default" if values["skins"]["default"] else None
            cape_existed = "cape" in values and bool(values["cape"])
        # parse skin hash
        if skin_type == "default":
            skin_hash = values["skins"]["default"]
        elif skin_type == "slim":
            skin_hash = values["skins"]["slim"]
        else:
            skin_hash = None
        skin_existed = bool(skin_hash)

        values.update(
            {
                "player_existed": player_existed,
                "skin_type": skin_type,
                "skin_existed": skin_existed,
                "cape_existed": cape_existed,
                "skin_hash": skin_hash,
            }
        )
        return values

    @classmethod
    async def get(cls, api_root: str, username: str):
        async with httpx.AsyncClient(base_url=api_root) as client:
            resp = (await client.get(f"{username}.json")).raise_for_status().json()
            if not resp:
                logger.warning(f"Player {username} not found.")
                return None
            return cls(**resp)
