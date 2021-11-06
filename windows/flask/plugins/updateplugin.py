import sqlite3
from config import peek_prefix

class Update_Plugin:
    def __init__(self,base_name,prefix,data_to_store,key_value):
        self.base_name = base_name
        self.data_to_store = data_to_store
        self.key_value = key_value
        self.db_prefix = prefix
        self.prefix = peek_prefix
        self.message = "Inserted"
    
    def update_table(self):
        c = sqlite3.connect(self.base_name+self.db_prefix)
        cursor = c.cursor()
        insert_query = "UPDATE {} SET urlvalue='{}' WHERE urlaskey='{}'".format(self.base_name, self.data_to_store, str(self.key_value).replace(self.prefix,"").replace(".html","").strip())
        cursor.execute(insert_query)
        c.commit()
        c.close()
        return self.message
