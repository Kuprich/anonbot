import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import or_
from sqlalchemy.orm import Session
from data.models import Base, Queue, Chat


class DbRepository:
    def __init__(self, url: str) -> None:
        self.engine = db.create_engine(url)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            Base.metadata.create_all(self.engine)

    def add_queue(self, chat_id):
        with Session(self.engine) as session, session.begin():
            session.add(Queue(chat_id=chat_id))

    def delete_queue(self, queue):
        with Session(self.engine) as session, session.begin():
            session.delete(queue)

    def get_chat(self):
        with Session(self.engine) as session:
            queue = session.query(Queue).one_or_none()
            return queue
    
    def get_chat_from_chat_id(self, chat_id): 
        with Session(self.engine) as session:
            return session.query(Queue).filter(Queue.chat_id == chat_id).one_or_none()

    def create_chat(self, chat_one, chat_two):
        with Session(self.engine) as session, session.begin():
            session.add(Chat(chat_one=chat_one, chat_two=chat_two))

    def get_active_chat(self, chat_id):
        with Session(self.engine) as session:
            return session.query(Chat).filter( (Chat.chat_one == str(chat_id)) | (Chat.chat_two == str(chat_id)) ).one_or_none()

    def delete_chat(self, chat):
        with Session(self.engine) as session, session.begin():
            session.delete(chat)
