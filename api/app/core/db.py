from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr


from app.core.config import settings

@as_declarative()
class Base:
    id: Any
    __name__: str
    __table_args__ = {"extend_existing": True}
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_size=32, max_overflow=64)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
