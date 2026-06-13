import datetime
import sqlite3

class SQLliteDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.create_table("apartments")
        self.create_table("valuable_offers")

    def create_table(self, table_name):
        sql_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                image TEXT,
                price REAL,
                price_per_m2 REAL,
                apartment_size REAL,
                created_at TEXT
            )
        '''
        self.cursor.execute(sql_query)
        self.conn.commit()

    def is_new_offer(self, url):
        self.cursor.execute("SELECT id FROM apartments WHERE url = ?", (url,))
        result = self.cursor.fetchone()
        return result is None

    def is_valuable_offer(self, price_per_m2):
        self.cursor.execute("SELECT AVG(price_per_m2) FROM apartments")
        avg_tuple = self.cursor.fetchone()

        if not avg_tuple or avg_tuple[0] is None:
            return False

        avg_value = avg_tuple[0]
        return price_per_m2 < avg_value * 0.85

    def insert_new_offer(self, offer_data, table_name):
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_query = f'''
                    INSERT INTO {table_name} (url, title, image, price, price_per_m2, apartment_size, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    '''
            self.cursor.execute(sql_query, (
                                    offer_data['url'],
                                    offer_data['title'],
                                    offer_data['image'],
                                    offer_data['price'],
                                    offer_data['price_per_m2'],
                                    offer_data['apartment_size'],
                                    now
                                ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def close_connection(self):
        self.conn.close()