from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )
    position: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="planned"
    )