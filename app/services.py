from app.models import JobApplication
from enum import Enum

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

applications = []
next_application_id = 1


def add_application(company, position):
    global next_application_id

    application = JobApplication(
        application_id=next_application_id,
        company=company,
        position=position
    )

    applications.append(application)
    next_application_id += 1

    return application


def get_all_applications():
    return applications


def find_application_by_id(application_id):
    for application in applications:
        if application.id == application_id:
            return application

    return None


def find_application_by_company(company_name):
    result = []

    for application in applications:
        if company_name.lower() in application.company.lower():
            result.append(application)

    return result


def update_application_status(application_id, new_status):
    if new_status not in ALLOWED_STATUSES:
        return UpdateStatusResult.INVALID_STATUS, None


    application = find_application_by_id(application_id)


    if application is None:
        return UpdateStatusResult.APPLICATION_NOT_FOUND, None

    application.status = new_status

    return UpdateStatusResult.UPDATED, application

def delete_application(application_id):
    application = find_application_by_id(application_id)

    if application is None:
        return False

    applications.remove(application)
    return True


def reset_applications():
    global next_application_id
    
    applications.clear()
    next_application_id = 1