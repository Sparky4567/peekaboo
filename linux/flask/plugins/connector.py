import sqlite3
from functools import lru_cache
class Base_Connector:
    def __init__(self,base_name,base_query,status_fetch_one,status_fetch_all,status_commit):
        self.base_name = base_name
        self.base_query = base_query
        self.status_fetch_one = status_fetch_one
        self.status_fetch_all = status_fetch_all
        self.status_commit = status_commit
    
    @lru_cache(maxsize=100)
    def connect_base(self):
        c = sqlite3.connect(self.base_name)
        cursor = c.cursor()
        cursor.execute(self.base_query)
        if(self.status_commit==True):
            c.commit()
            c.close()
        if(self.status_fetch_one==True):
            res = cursor.fetchone()
            c.close()
            return res
        if(self.status_fetch_all==True):
            res = cursor.fetchall()
            c.close()
            return res
        c.close()



