import pymongo
import certifi

def db_connect():

    db = pymongo.MongoClient("mongodb+srv://almasyarkhan007:1eiygny3nsMA8kM0@cluster1.voubafg.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = db["fastapi_db"] 
    return db












