from .minirag_base import sqlbase
from sqlalchemy import Integer, String, func, DateTime, Column, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid


class jobposting(sqlbase):
    __tablename__ = "jobpostings"
    
    jobposting_id = Column(Integer, primary_key=True, autoincrement=True)
    jobposting_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique= True, nullable=False)

    job_title = Column(String, nullable=False, server_default='Unknown')
    company_name = Column(String, nullable=False, server_default='Unknown')
    skills = Column(ARRAY(String), nullable=False, server_default='{}')  # Empty array as default
    recruiter_email = Column(String, nullable=True)
    post_metadata = Column(JSONB, nullable=True)

    jobposting_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


    user = relationship("User", back_populates="jobposting")
