'''
Copyright 2021 Makiyu-py

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from os import environ
import ast
import hashlib
import collections
import logging


class DBShortCuts:
    def __init__(self, connection, document_name):
        """
        Our init function, sets up the conenction to the specified document
        Params:
         - connection (Mongo Connection) : Our database connection
         - documentName (str) : The document this instance should be
        """
        self.db = connection[document_name]
        self.iters = int(environ.get("ITERATE_ENCRYPTION_COUNT"))
        self.logger = logging.getLogger(__name__)

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
        e = kwargs.get("id_enc", False)  # I gave up on naming the vars 'enc_mode' over-and-over again smh
        if e:
            dict["_id"] = self.encrypt(dict['_id'])

        if await self.__get_raw(dict["_id"]) != None:
            await self.update_by_id(dict)
        else:
            await self.db.insert_one(dict)

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
        
        not_supported = [set, dict, hex]  # there's so much more but that's the only stuff
        								  # that I actually use lol
            
        if isinstance(item, [ns for ns in not_supported]):
            raise TypeError(f"Expected the 2nd parameter of `conjoin` as a string/list, not '{type(item).__name__}'")
            
        if not isinstance(item, list) and not isinstance(item, tuple):
            item = [item]
            
        elif isinstance(item, tuple):  # MongoDB does not allow tuples. ;(
            item = list(item)
        
        enc_mode = kwargs.get("encrypt_id", False)
        id = self.encrypt(id) if enc_mode else id
        await self.db.update_one({"_id": id}, {"$addToSet": {field: {"$each": amount}}})

            
           
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

    def encrypt(self, i: str):
        """
        Iterates the given string to a sha256 string [REDACTED] times

        Params:
         - i: str - The string you want to iterate on
        """
        i = str(i)
        for _ in range(self.iters):
            i = hashlib.sha256(i.encode()).hexdigest()
            #i = hashlib.sha256(bytes(i, 'utf-8')).hexdigest()
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
