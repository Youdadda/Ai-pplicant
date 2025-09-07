from sqlalchemy import Column , Integer, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from bson.objectid import ObjectId
from sqlalchemy.orm import relationship
from typing import Optional
from .minirag_base import sqlbase
import uuid

class Asset(sqlbase):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    asset_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique= True, nullable=False)

    asset_type = Column(String, nullable= False)
    asset_name = Column(String, nullable= False)
    asset_size = Column(Integer, nullable= False)
    asset_config = Column(JSONB, nullable= True)

    asset_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    project = relationship("Project", back_populates="assets")
    chunks = relationship("Chunk",back_populates="asset")