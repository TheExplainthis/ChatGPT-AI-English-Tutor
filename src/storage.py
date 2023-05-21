from tinydb import TinyDB, where
from BetterJSONStorage import BetterJSONStorage
from pathlib import Path


class FileStorage:
    def __init__(self, file_name):
        self.path = Path(file_name)

    def get(self, id):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            data = db.search(where('user_id') == id)
        return data

    def save(self, data):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            db.insert(data)

    def remove(self, id):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            db.remove(where('user_id') == id)


class Storage:
    def __init__(self, storage):
        self.storage = storage

    def get(self, id):
        return self.storage.get(id)

    def save(self, data):
        self.storage.save(data)

    def remove(self, id):
        self.storage.remove(id)