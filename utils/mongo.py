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

import ast
import collections
import hashlib
import logging
from os import environ


class DBShortCuts:
    def __init__(self, connection, document_name):
        """
        Our init function, sets up the conenction to the specified document
        Params:
         - connection (Mongo Connection) : Our database connection
         - documentName (str) : The document this instance should be
        """
        self.db = connection[document_name]
        self._db_name = document_name
        self.iters = int(environ.get("ITERATE_ENCRYPTION_COUNT"))
        self.logger = logging.getLogger(__name__)
        self.kash = None
        self.inited_kash = False

    # <-- Attributes -->
    @property
    def db_name(self):
        return self._db_name

    # <-- Pointer Methods -->
    async def update(self, dict, **options):
        """
        For simpler calls, points to self.update_by_id
        """
        await self.update_by_id(dict, **options)

    async def get_by_id(self, id, **options):
        """
        This is essentially find_by_id so point to that
        """
        return await self.find_by_id(id)

    async def find(self, id, **options):
        """
        For simpler calls, points to self.find_by_id
        """
        return await self.find_by_id(id)

    async def delete(self, id, **options):
        """
        For simpler calls, points to self.delete_by_id
        """
        await self.delete_by_id(id, **options)

    # <-- Actual Methods -->
    async def find_by_id(self, id, **kwargs):
        """
        Returns the data found under `id`
        Params:
         -  id () : The id to search for
         -  id_enc (bool) : Iterates the ID to SHA256 a *few* times if wanted to
        Returns:
         - None if nothing is found
         - If somethings found, return that
        """
        enc_mode = kwargs.get("id_enc", False)
        id = id if not enc_mode else self.encrypt(id)

        if self.inited_kash:
            if thing_from_kas := self.get_item_from_kash(id):
                return thing_from_kas
        return await self.db.find_one({"_id": id})

    async def delete_by_id(self, id, **kwargs):
        """
        Deletes all items found with _id: `id`
        Params:
         -  id () : The id to search for and delete
         -  id_enc (bool) : Iterates the ID to SHA256 a *few* times if wanted to
        """
        if not await self.find_by_id(id):
            return

        enc_mode = kwargs.get("id_enc", False)

        id = self.encrypt(id) if enc_mode else id
        await self.db.delete_many({"_id": id})

    async def insert(self, dict, **kwargs):
        """
        insert something into the db
        Params:
        - dict (Dictionary) : The Dictionary to insert
        - enc_id (bool) : Iterates the ID of the given dict to SHA256 a *few* times if wanted to
        """
        # Check if its actually a Dictionary
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected Dictionary.")

        # Always use your own _id
        if not dict["_id"]:
            raise KeyError("_id not found in supplied dict.")

        enc_mode = kwargs.get("enc_id", False)
        if enc_mode:
            dict["_id"] = self.encrypt(dict["_id"])

        await self.db.insert_one(dict)

        if self.inited_kash:
            self.kash.append(dict)

    async def upsert(self, dict, **kwargs):
        """
        Makes a new item in the document, if it already exists
        it will update that item instead
        This function parses an input Dictionary to get
        the relevant information needed to insert.
        Supports inserting when the document already exists
        Params:
         - dict (Dictionary) : The dict to insert
         -  id_enc (bool) : Iterates the ID to SHA256 a *few* times if wanted to
        """
        e = kwargs.get(
            "id_enc", False
        )  # I gave up on naming the vars 'enc_mode' over-and-over again smh
        if e:
            dict["_id"] = self.encrypt(dict["_id"])

        if await self.__get_raw(dict["_id"]) is not None:
            await self.update_by_id(dict)
        else:
            await self.db.insert_one(dict)
            if self.inited_kash:
                self.kash.append(dict)

    async def update_by_id(self, dict, **kwargs):
        """
        For when a document already exists in the data
        and you want to update something in it
        This function parses an input Dictionary to get
        the relevant information needed to update.
        Params:
         - dict (Dictionary) : The dict to insert
         - encrypt_id (Boolean) : If you want to encrypt the id of the dict
        """
        # Check if its actually a Dictionary
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected Dictionary.")

        # Always use your own _id
        if not dict["_id"]:
            raise KeyError("_id not found in given dict.")

        if not await self.find_by_id(dict["_id"]):
            return

        enc_mode = kwargs.get("encrypt_id", False)
        id = dict["_id"] if not enc_mode else self.encrypt(dict["_id"])
        dict.pop("_id")
        await self.db.update_one({"_id": id}, {"$set": dict})

    async def unset(self, dict, **kwargs):
        """
        For when you want to remove a field from
        a pre-existing document in the collection
        This function parses an input Dictionary to get
        the relevant information needed to unset.
        Params:
         - dict (Dictionary) : Dictionary to parse for info
         - encrypt_id (Boolean) : If you want to encrypt the id of the dict
        """
        # Check if its actually a Dictionary
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected Dictionary.")

        # Always use your own _id
        if not dict["_id"]:
            raise KeyError("_id not found in supplied dict.")

        if not await self.find_by_id(dict["_id"]):
            return

        enc_mode = kwargs.get("encrypt_id", False)
        id = dict["_id"] if not enc_mode else self.encrypt(dict["_id"])
        dict.pop("_id")
        await self.db.update_one({"_id": id}, {"$unset": dict})

    async def conjoin(self, id, item, field, amount, **kwargs):
        """
        appends the given item/s to `field`
        Params:
        - id () : The id to search for
        - item (list/str) : item/s to append to the field
        - field () : field to append the item/s on
        - encrypt_id (Boolean) : Encrypts the id 20 times to SHA265
        """
        if not await self.find_by_id(id):
            return

        not_supported = [
            set,
            dict,
            hex,
        ]  # there's so much more but that's the only stuff
        # that I actually use lol

        if isinstance(item, [ns for ns in not_supported]):
            raise TypeError(
                f"Expected the 2nd parameter of `conjoin` as a string/list, not '{type(item).__name__}'"
            )

        if not isinstance(item, list) and not isinstance(item, tuple):
            item = [item]

        elif isinstance(item, tuple):  # MongoDB does not allow tuples. ;(
            item = list(item)

        enc_mode = kwargs.get("encrypt_id", False)
        id = self.encrypt(id) if enc_mode else id
        await self.db.update_one({"_id": id}, {"$addToSet": {field: {"$each": amount}}})
        if self.inited_kash:
            self.kash[self.kash.index(self.get_item_from_kash(id))][
                field
            ] = amount  # that is long lmao

    async def increment(self, id, amount, field, **kwargs):
        """
        Increment a given `field` by `amount`
        Params:
        - id () : The id to search for
        - amount (int) : Amount to increment by
        - field () : field to increment
        - encrypt_id (Boolean) : Encrypts the id 20 times to SHA265
        """
        if not await self.find_by_id(id):
            return

        enc_mode = kwargs.get("encrypt_id", False)
        id = self.encrypt(id) if enc_mode else id
        await self.db.update_one({"_id": id}, {"$inc": {field: amount}})
        if self.inited_kash:
            self.kash[self.kash.index(self.get_item_from_kash(id))][field] += amount

    async def get_all(self):
        """
        Returns a list of all data in the document
        """
        data = []
        async for document in self.db.find({}):
            data.append(document)
        return data

    # <-- Private methods -->
    async def __get_raw(self, id):
        """
        An internal private method used to eval certain checks
        within other methods which require the actual data
        """
        return await self.db.find_one({"_id": id})

    def get_item_from_kash(self, id_):
        if not self.inited_kash:
            return None
        try:
            return next(item for item in self.kash if item["_id"] == id_)
        except StopIteration:
            return None
        except KeyError:
            return None

    def encrypt(self, i: str):
        """
        Iterates the given string to a sha256 string [REDACTED] times

        Params:
         - i: str - The string you want to iterate on
        """
        i = str(i)
        for _ in range(self.iters):
            i = hashlib.sha256(i.encode()).hexdigest()
            # i = hashlib.sha256(bytes(i, 'utf-8')).hexdigest()
        return i

    # <-- Custom methods -->
    async def get_document(self, id, **kwargs):
        """
        Gives you a dictionary all of the info in the document id
        given.
        Params:
        - id () : The id you want to get info on
        - encrypt_id (Boolean) : Encrypts the id 20 times to SHA265
        Returns:
        - False if id not in the database
        - If it is, it'll return the document info as a dictionary
        """
        enc_mode = kwargs.get("encrypt_id", False)
        id = self.encrypt(id) if enc_mode else id
        async for the_dict in self.db.find({"_id": id}):
            # Check if its actually a Dictionary. If not, convert it to one!
            if not isinstance(the_dict, collections.abc.Mapping):
                the_dict = ast.literal_eval(the_dict)

        try:
            return the_dict
        except UnboundLocalError:
            return False

    async def init_kash(self):
        """
        Initializes the cache.
        """
        cache = await self.get_all()
        self.kash = cache
        self.inited_kash = True
