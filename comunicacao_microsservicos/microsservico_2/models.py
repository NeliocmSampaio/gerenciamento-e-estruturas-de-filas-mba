from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class UserModel(Base):
    __tablename__ = "tb_users" 

    id = Column(UUID, primary_key=True, index=True)
    nome = Column(String, nullable=False) 
    email = Column(String, unique=True, nullable=False)
