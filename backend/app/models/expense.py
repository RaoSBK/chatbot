import uuid
from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Text, Uuid, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import TimestampMixin, SoftDeleteMixin
from datetime import datetime, timezone

class Expense(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "expenses"

    expense_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    payment_method = Column(String(100), nullable=True)
    transaction_date = Column(Date, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="expenses")
