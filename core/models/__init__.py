"""
This file is part of KIGM-Discord-Bot.

KIGM-Discord-Bot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

KIGM-Discord-Bot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with KIGM-Discord-Bot.  If not, see <https://www.gnu.org/licenses/>.
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from umongo import Document, fields
from umongo.frameworks import MotorAsyncIOInstance


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


def init_models(db: AsyncIOMotorDatabase):
    global Guild, Economy
    instance = MotorAsyncIOInstance(db)
    Guild = instance.register(Guild)
    Economy = instance.register(Economy)
