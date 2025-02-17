import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            recoards = list(json.loads(data.T.to_json()).values())
            return recoards
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self, recoards, database, collection):
        try:
            self.dabtabase = database
            self.collection = collection
            self.recoards = recoards

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.dabtabase]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.recoards)
            return len(self.recoards)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "PROJECT"
    Collection = "NetworkData"
    network_obj = NetworkDataExtract()
    recoards = network_obj.csv_to_json_converter(file_path=FILE_PATH)
    print(recoards)
    no_of_recoards = network_obj.insert_data_mongodb(recoards=recoards, database=DATABASE, collection=Collection)
    print(f"Total Number of Recoards Inserted: {no_of_recoards}")



