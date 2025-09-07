from datetime import datetime
from typing import Self

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, field_serializer

from commspt_bot_avilla.utils.setting_manager import S_


class UIDMapping(BaseModel):
    uid: int
    qq: int
    last_update: datetime | None = Field(default_factory=datetime.now)
    qmail_verified: bool | None = False

    @field_serializer("last_update")
    def serialize_last_update(self, value: datetime):
        return value.timestamp()

    async def update(self) -> None:
        mongo = AsyncIOMotorClient(S_.db_mongo.url)
        coll = mongo["commspt-bot"]["uid"]
        query = {"qq": self.qq}
        data = self.model_dump()
        if await coll.find_one(query):
            _ = await coll.update_one(query, {"$set": data})
        else:
            _ = await coll.insert_one(data)
        mongo.close()

    @classmethod
    async def fetch(cls, qq: int | None = None, uid: int | None = None) -> Self | None: 
        mongo = AsyncIOMotorClient(S_.db_mongo.url)
        coll = mongo["commspt-bot"]["uid"]
        if qq:
            if data := await coll.find_one({"qq": qq}):
                return cls(**data)
        elif uid and (data := await coll.find_one({"uid": uid})):
            return cls(**data)
        mongo.close()
        return None
