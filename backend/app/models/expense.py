import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, Date, DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import relationship
from app.core.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    merchant = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="expenses")
