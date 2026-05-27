import uuid
from sqlalchemy import Column, String, Numeric, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import TimestampMixin

class Budget(Base, TimestampMixin):
    __tablename__ = "budgets"

    budget_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    monthly_limit = Column(Numeric(12, 2), nullable=False)
    current_spending = Column(Numeric(12, 2), default=0.00, nullable=False)
    remaining_amount = Column(Numeric(12, 2), default=0.00, nullable=False)

    # Relationships
    user = relationship("User", back_populates="budgets")
