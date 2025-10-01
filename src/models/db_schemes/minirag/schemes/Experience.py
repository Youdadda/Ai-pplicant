from sqlalchemy import Column , Integer, String, DateTime, func, ForeignKey, Date
from sqlalchemy.types import ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from bson.objectid import ObjectId
from sqlalchemy.orm import relationship
from typing import Optional
from .minirag_base import sqlbase
import uuid

class Experience(sqlbase):

    __tablename__ = "experience"

    experience_id = Column(Integer, primary_key=True, autoincrement=True)
    experience_asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)
    experience_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    section_type = Column(String, nullable = False)
    title = Column(String, nullable = False)
    company = Column(String, nullable=True)
    experience_type = Column(String , nullable= False)
    skills = Column(ARRAY(String), nullable = False)
    description = Column(String, nullable=False)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    experience_metadata = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    asset = relationship("Asset", back_populates="experiences")
    user = relationship("User", back_populates="experiences")