from enum import Enum

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import JobApplication


class UpdateStatusResult(Enum):
    UPDATED = "updated"
    INVALID_STATUS = "invalid_status"
    APPLICATION_NOT_FOUND = "application_not_found"


ALLOWED_STATUSES = {
    "planned",
    "applied",
    "interview",
    "offer",
    "rejected",
}



def add_application(
    db: Session,
    company: str,
    position: str,
) -> JobApplication:
    application = JobApplication(
        company=company,
        position=position,
        status="planned",
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_all_applications(
    db: Session,
) -> list[JobApplication]:
    statement = select(JobApplication).order_by(JobApplication.id)

    return list(db.scalars(statement).all())


def find_application_by_id(
    db: Session,
    application_id: int,
) -> JobApplication | None:
    return db.get(JobApplication, application_id)


def find_application_by_company(
    db: Session,
    company_name: str,
) -> list[JobApplication]:
    statement = (
        select(JobApplication)
        .where(
            JobApplication.company.ilike(
                f"%{company_name}%"
            )
        )
        .order_by(JobApplication.id)
    )

    return list(db.scalars(statement).all())


def update_application_status(
    db: Session,
    application_id: int,
    new_status: str,
) -> tuple[UpdateStatusResult, JobApplication | None]:
    if new_status not in ALLOWED_STATUSES:
        return UpdateStatusResult.INVALID_STATUS, None

    application = find_application_by_id(
        db,
        application_id,
    )

    if application is None:
        return UpdateStatusResult.APPLICATION_NOT_FOUND, None

    application.status = new_status

    db.commit()
    db.refresh(application)

    return UpdateStatusResult.UPDATED, application

def delete_application(
    db: Session,
    application_id: int,
) -> bool:
    application = find_application_by_id(
        db,
        application_id,
    )

    if application is None:
        return False

    db.delete(application)
    db.commit()

    return True

