import tqdm

from database import MongoDatabase, TinyDatabase


def tiny2mongo():
    """
    Export data from TinyDB to MongoDB.
    """
    tiny_database = TinyDatabase()
    mongo_database = MongoDatabase()

    for stock in tqdm.tqdm(tiny_database.all()):
        mongo_database.upsert(stock)