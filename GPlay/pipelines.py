import sqlite3
from jsonschema import validate



class SqlitePipeline(object):



    def __init__(self):
        self.create_connection()
        self.create_table()



    def create_connection(self):
        self.conn = sqlite3.connect("gplay_data.db")
        self.curr = self.conn.cursor()



    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS gplay_data""")
        self.curr.execute("""
            CREATE TABLE gplay_data(
                category TEXT,
                subcategory TEXT,
                title TEXT,
                subtitle TEXT,
                product_number TEXT,
                price REAL
            )
        """)



    def process_item(self, item, spider):
        self.store_db(item)
        return item



    def store_db(self, item):
        data = {
            "category": item["category"],
            "subcategory": item["subcategory"],
            "title": item["title"],
            "subtitle": item["subtitle"],
            "product_number": item["product_number"],
            "price": item["price"]
        }

        schema = {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "subcategory": {"type": "string"},
                    "title": {"type": "string"},
                    "subtitle": {"type": "string"},
                    "product_number": {"type": "string"},
                    "price": {"type": "number"}
                },
                "required": ["category",
                             "subcategory",
                             "title",
                             "subtitle",
                             "product_number",
                             "price"]
            }

        if validate(instance=data, schema=schema) == None:
            self.curr.execute("""INSERT INTO gplay_data VALUES(?, ?, ?, ?, ?, ?)""", (
                item["category"],
                item["subcategory"],
                item["title"],
                item["subtitle"],
                item["product_number"],
                item["price"]
            ))
            self.conn.commit()
