import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, Date, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from app.core.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    target_amount = Column(Numeric(12, 2), nullable=False)
    current_amount = Column(Numeric(12, 2), default=0.00, nullable=False)
    target_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="goals")
