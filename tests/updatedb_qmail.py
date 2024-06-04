import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from rich import print

from commspt_bot_avilla.models.littleskin_api import LittleSkinUser
from commspt_bot_avilla.models.mongodb_data import UIDMapping
from commspt_bot_avilla.utils.setting_manager import S_


async def main():
    mongo = AsyncIOMotorClient(S_.db_mongo.url)
    coll = mongo["commspt-bot"]["uid"]
    async for data in coll.find({"qmail_verified": False}):
        mapping = UIDMapping(**data)
        ltsk_user = await LittleSkinUser.qmail_api(mapping.qq)
        if ltsk_user:
            mapping.uid = ltsk_user.uid
            mapping.qmail_verified = True
            print(mapping)
            await mapping.update()
    mongo.close()


asyncio.run(main())
