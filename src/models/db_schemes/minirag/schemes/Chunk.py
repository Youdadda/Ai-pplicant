from .minirag_base import sqlbase
from sqlalchemy import Integer, String, func, DateTime, Column, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid


class Chunk(sqlbase):
    __tablename__ = "chunks"
    
    chunk_id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique= True, nullable=False)

    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    skills = Column(ARRAY, nullable=False)
    recruiter_email = Column(String, nullable=True)
    chunk_metadata = Column(JSONB, nullable=True)

    chunk_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    chunk_asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


    project = relationship("Project", back_populates="chunk")
    asset = relationship("Asset", back_populates="chunks")