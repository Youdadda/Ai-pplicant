from sqlalchemy import Column , Integer, DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .minirag_base import sqlbase
import uuid
class User(sqlbase):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique= True, nullable=False)


    user_name = Column(String, nullable=True)
    user_email = Column(String, nullable= True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    assets = relationship("Asset", back_populates="user")
    jobposting = relationship("jobposting", back_populates="user")
    experiences = relationship("Experience", back_populates="user")