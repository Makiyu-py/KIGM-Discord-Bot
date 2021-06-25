from motor.motor_asyncio import AsyncIOMotorClient
from umongo.frameworks import MotorAsyncIOInstance
from umongo import Document, fields

class Guild(Document):
    gid = fields.IntField(required=True, attribute="_id")
    prefix = fields.StrField(default="&", attribute="Bot Prefix")
    GARole = fields.IntField()

    class Meta:
        collection_name = "G_Config"

class Economy(Document):
    user_id = fields.IntField(required=True, attribute="_id")
    bank = fields.IntField()
    purse = fields.IntField()

    class Meta:
        collection_name = "Economy"


def init_models(db: AsyncIOMotorClient):
    global Guild, Economy
    instance = MotorAsyncIOInstance(db)
    Guild = instance.register(Guild)
    Economy = instance.register(Economy)