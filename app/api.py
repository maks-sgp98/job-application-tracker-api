from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import db_models
from app.database import Base, engine, get_db
from app.schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
)
from app.services import (
    UpdateStatusResult,
    add_application,
    delete_application,
    find_application_by_company,
    find_application_by_id,
    get_all_applications,
    update_application_status,
)

Base.metadata.create_all(bind=engine)

DatabaseSession = Annotated[Session, Depends(get_db)]

app = FastAPI(
    title="Job Application Tracker API",
    description="API for tracking job applications",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "message": "Job Application Tracker API",
        "status": "running",
    }


@app.get(
    "/applications",
    response_model=list[ApplicationResponse],
)
def read_applications(db: DatabaseSession):
    return get_all_applications(db)


@app.post(
    "/applications",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    data: ApplicationCreate,
    db: DatabaseSession,
):
    return add_application(
        db=db,
        company=data.company,
        position=data.position,
    )


@app.get(
    "/applications/search/by-company",
    response_model=list[ApplicationResponse],
)
def search_applications_by_company(
    db: DatabaseSession,
    company: str = Query(min_length=1),
):
    return find_application_by_company(
        db,
        company,
    )


@app.get(
    "/applications/{application_id}",
    response_model=ApplicationResponse,
)
def read_application(
    application_id: int,
    db: DatabaseSession,
):
    application = find_application_by_id(
        db,
        application_id,
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application


@app.patch(
    "/applications/{application_id}/status",
    response_model=ApplicationResponse,
)
def change_application_status(
    application_id: int,
    data: ApplicationStatusUpdate,
    db: DatabaseSession,
):
    result, application = update_application_status(
        db,
        application_id,
        data.status.lower(),
    )

    if result is UpdateStatusResult.INVALID_STATUS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid application status",
        )

    if result is UpdateStatusResult.APPLICATION_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application


@app.delete(
    "/applications/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_application(
    application_id: int,
    db: DatabaseSession,
):
    deleted = delete_application(
        db,
        application_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return None
