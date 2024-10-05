from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class Queue(Base):
    __tablename__ = 'queue'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        return f'Queue(id={self.id}, chat_id={self.chat_id})'


class Chat(Base):
    __tablename__ = 'chat'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_one: Mapped[str] = mapped_column(String(20))
    chat_two: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        return f'Chat(id={self.id}, chat_one={self.chat_one}, chat_two={self.chat_two})'
