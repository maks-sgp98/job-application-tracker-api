from fastapi import FastAPI, HTTPException, Query, status

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
def read_applications():
    return get_all_applications()


@app.post(
    "/applications",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(data: ApplicationCreate):
    return add_application(
        company=data.company,
        position=data.position,
    )


@app.get(
    "/applications/{application_id}",
    response_model=ApplicationResponse,
)
def read_application(application_id: int):
    application = find_application_by_id(application_id)

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
):
    result, application = update_application_status(
        application_id,
        data.status.lower(),
    )

    if result is UpdateStatusResult.INVALID_STATUS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
def remove_application(application_id: int):
    deleted = delete_application(application_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return None


@app.get(
    "/applications/search/by-company",
    response_model=list[ApplicationResponse],
)
def search_applications_by_company(
    company: str = Query(min_length=1),
):
    return find_application_by_company(company)