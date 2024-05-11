from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import AnyHttpUrl
from typing import Annotated
from cookit.pyd import type_validate_json
from datetime import datetime
import httpx


class CustomSkinLoaderLatest(BaseModel):

    class Downloads(BaseModel):
        fabric: Annotated[AnyHttpUrl, str] = Field(alias="Fabric")
        forge: Annotated[AnyHttpUrl, str] = Field(alias="Forge")
        forgeactive: Annotated[AnyHttpUrl, str] = Field(alias="ForgeActive")

        @property
        def generate_download_text(self) -> str:
            return f"Fabric: {self.fabric}\nForge: {self.forge}\nForge Active: {self.forgeactive}"

    version: str
    downloads: Downloads

    @classmethod
    async def get(cls):
        async with httpx.AsyncClient() as client:
            return type_validate_json(
                cls,
                (
                    await client.get(
                        "https://csl-1258131272.cos.ap-shanghai.myqcloud.com/latest.json"
                    )
                )
                .raise_for_status()
                .text,
            )


class AuthlibInjectorLatest(BaseModel):

    class CheckSums(BaseModel):
        sha256: str

    build_number: int
    version: str
    release_time: datetime
    download_url: Annotated[AnyHttpUrl, str]
    checksums: CheckSums

    @classmethod
    async def get(cls):
        async with httpx.AsyncClient() as client:
            return type_validate_json(
                cls,
                (
                    await client.get(
                        "https://authlib-injector.yushi.moe/artifact/latest.json"
                    )
                )
                .raise_for_status()
                .text,
            )
