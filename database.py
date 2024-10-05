import sqlite3


class Database:
    def __init__(self, db_name) -> None:
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        
    def add_queue(self, user_id):#
        with self.connection: 
            return self.cursor.execute(f"INSERT INTO queue (chat_id) VALUES ({user_id})")
    
    def delete_queue(self, user_id):#
        with self.connection: 
            return self.cursor.execute(f"DELETE FROM queue WHERE chat_id = {user_id}")
        
    def get_chat(self): 
        with self.connection: 
            user_id = self.cursor.execute("SELECT * FROM queue").fetchone()
            return user_id
        
    def get_chat_from_chat_id(self, chat_id): 
        with self.connection: 
            chat_id = self.cursor.execute(f"SELECT * FROM queue WHERE chat_id = {chat_id}").fetchone()
            return chat_id
    
    def create_chat(self, chat_one, chat_two): 
        with self.connection: 
            self.cursor.execute(f"INSERT INTO chats (chat_one, chat_two) VALUES ({chat_one}, {chat_two})")
            
    def delete_chat(self, chat_id):
        with self.connection: 
            self.cursor.execute(f"DELETE FROM chats WHERE id = {chat_id}")
            
    def get_active_chat(self, user_id): 
        with self.connection: 
            chat = self.cursor.execute(f"SELECT * FROM chats WHERE chat_one = {user_id} or chat_two = {user_id}").fetchone()
            return chat
            
        
        