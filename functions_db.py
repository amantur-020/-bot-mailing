import sqlite3

class FunctionsDB:

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.create_db()

    def create_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS newsletters(
            keyword varchar(100),
            message_id integer,
            time integer
        )""")
        self.conn.commit()

    def add_db(self, keyword, message_id, time):
        self.cursor.execute("INSERT INTO newsletters (keyword, message_id, time) VALUES (?, ?, ?)",
                            (keyword, message_id, time))
        self.conn.commit()

    def delete_db(self, keyword):
        self.cursor.execute("SELECT keyword FROM newsletters WHERE keyword=?", (keyword,))
        existing_keyword = self.cursor.fetchone()
        if existing_keyword:
            self.cursor.execute("DELETE FROM newsletters WHERE keyword=?", (keyword,))
            self.conn.commit()
            return True
        else:
            return False
    
    def get_record_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM newsletters")
        result = self.cursor.fetchone()
        return result[0] if result is not None else 0
    
    def delete_all_records(self):
        self.cursor.execute("DELETE FROM newsletters")
        self.conn.commit()
        
    def get_message_id_by_time(self, time):
        self.cursor.execute("SELECT message_id FROM newsletters WHERE time=?", (time,))
        result = self.cursor.fetchone()
        return int(result[0]) if result is not None else None

    def close(self):
        self.conn.close()
