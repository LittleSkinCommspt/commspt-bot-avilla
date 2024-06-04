import hashlib

import httpx
from pydantic import BaseModel


class LegacyApi(BaseModel):
    image_bytes: bytes | None = None
    sha256: str | None = None
    skin_preview: bytes | None = None
    texture_type: str
    existed: bool = True

    @classmethod
    async def get(cls, api_root: str, username: str, texture_type: str):
        async with httpx.AsyncClient(base_url=api_root, follow_redirects=True) as client:
            image_bytes = (await client.get(url=f"{api_root}/{texture_type}/{username}.png")).raise_for_status().content
            sha256 = hashlib.sha256(image_bytes).hexdigest()
            return cls(
                image_bytes=image_bytes,
                sha256=sha256,
                skin_preview=(await client.get(url=f"/preview/hash/{sha256}?png")).raise_for_status().content,
                texture_type=texture_type,
            )
