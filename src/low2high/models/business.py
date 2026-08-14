from sqlalchemy import Column, String, Float, Integer, DateTime
from datetime import datetime
import uuid
from .database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    name = Column(String, index=True, nullable=False)
    phone = Column(String, index=True, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    category = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, nullable=True)
    website = Column(String, nullable=True)
    place_id = Column(String, index=True, nullable=True)
    source = Column(String, default="google_maps")
    created_at = Column(DateTime, default=datetime.utcnow)
    audit_grade = Column(String, nullable=True)
    audit_data = Column(String, nullable=True)
