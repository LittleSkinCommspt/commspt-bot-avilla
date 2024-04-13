from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from utils.setting_manager import S_


async def write_uid_db(uid: int | str, qq: int | str):
    # make sure int
    uid = int(uid) if not isinstance(uid, int) else uid
    qq = int(qq) if not isinstance(qq, int) else qq

    mongo = AsyncIOMotorClient(S_.db_mongo.url)
    coll = mongo["commspt-bot"]["uid"]
    i = await coll.find_one({"qq": qq})

    r = {"uid": uid, "qq": qq, "last_update": datetime.now().timestamp()}

    if i:
        await coll.update_one({"qq": qq}, {"$set": r})
    else:
        await coll.insert_one(r)

    mongo.close()


async def get_uid_db(qq: int | str) -> int | None:
    # make sure int
    qq = int(qq) if not isinstance(qq, int) else qq

    mongo = AsyncIOMotorClient(S_.db_mongo.url)
    coll = mongo["commspt-bot"]["uid"]
    i = await coll.find_one({"qq": qq})

    mongo.close()

    return i["uid"] if i else None
