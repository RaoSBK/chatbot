import uuid
from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Uuid, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.mixins import TimestampMixin, SoftDeleteMixin

class Goal(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "goals"

    goal_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_name = Column(String(255), nullable=False, index=True)
    target_amount = Column(Numeric(12, 2), nullable=False)
    saved_amount = Column(Numeric(12, 2), default=0.00, nullable=False)
    target_date = Column(Date, nullable=False, index=True)
    progress_percentage = Column(Float, default=0.0, nullable=False)
    status = Column(String(50), default="active", nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="goals")
