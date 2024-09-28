from datetime import datetime
from typing import Annotated

import httpx
from pydantic import AliasGenerator, BaseModel, ConfigDict, TypeAdapter, alias_generators
from pydantic.fields import Field
from pydantic.networks import AnyHttpUrl


class CustomSkinLoaderLatest(BaseModel):
    class Downloads(BaseModel):
        fabric: Annotated[AnyHttpUrl, str] = Field(alias="Fabric")
        forge: Annotated[AnyHttpUrl, str] = Field(alias="Forge")
        forgeactive: Annotated[AnyHttpUrl, str] = Field(alias="ForgeActive")

        @property
        def generate_download_text(self) -> str:
            return f"Fabric > {self.fabric}\nForge > {self.forge}\nForge Active > {self.forgeactive}"

    version: str
    downloads: Downloads

    @classmethod
    async def get(cls):
        """获取 CustomSkinLoader 最新版本信息

        Returns:
            CustomSkinLoaderLatest: CustomSkinLoader 最新版本信息
        """
        async with httpx.AsyncClient() as client:
            return cls(
                **(await client.get("https://api.github.com/repos/CustomSkinLoader/CustomSkinLoader/releases/latest"))
                .raise_for_status()
                .json(),
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
        """获取 Authlib-Injector 最新版本信息

        Returns:
            AuthlibInjectorLatest: Authlib-Injector 最新版本信息
        """
        async with httpx.AsyncClient() as client:
            return cls(
                **(await client.get("https://authlib-injector.yushi.moe/artifact/latest.json"))
                .raise_for_status()
                .json()
            )


class LibericaJavaLatest(BaseModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=alias_generators.to_camel))
    #
    bitness: int
    latest_lts: bool = Field(alias="latestLTS")
    update_version: int
    download_url: Annotated[AnyHttpUrl, str]
    latest_in_feature_version: bool
    lts: bool = Field(alias="LTS")
    bundle_type: str
    feature_version: int
    package_type: str
    fx: bool = Field(alias="FX")
    ga: bool = Field(alias="GA")
    architecture: str
    latest: bool
    extra_version: int
    build_version: int
    eol: bool = Field(alias="EOL")
    os: str
    interim_version: int
    version: str
    sha1: str
    filename: str
    installation_type: str
    size: int
    patch_version: int
    tck: bool = Field(alias="TCK")
    update_type: str

    @property
    def download_url_mirror(self):
        return f"https://download.bell-sw.com/java/{self.version}/{self.filename}"

    @classmethod
    async def get(
        cls,
        **kwargs,
    ):
        """获取 Liberica Java 版本信息

        参考 [BellSoft 官方 API 文档](https://api.bell-sw.com/api.html#/Binaries/get_liberica_releases)。

        Returns:
            List[LibericaJavaLatest]: Liberica Java 版本信息列表
        """

        libereca_releases = TypeAdapter(list[cls])

        for key in kwargs:
            kwargs[key.replace("_", "-")] = kwargs.pop(key)  # noqa: B909
        async with httpx.AsyncClient() as client:
            return libereca_releases.validate_python(
                (
                    await client.get(
                        "https://api.bell-sw.com/v1/liberica/releases",
                        params=kwargs,
                    )
                )
                .raise_for_status()
                .json(),
            )
