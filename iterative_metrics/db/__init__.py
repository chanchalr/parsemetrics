from abc import ABCMeta, abstractmethod
import json
import os
import hashlib
from git.objects.commit import Commit
from  . import postgresdb
def getDb(dbConfig):
    print(dbConfig)
    if dbConfig["type"] == "postgres":
        return postgresdb.postgres_db("postgres","postgres",dbConfig)
    else:
        raise NotImplementedError