import pytest

from app.services import(
    add_application,
    get_all_applications,
    find_application_by_id,
    delete_application,
    reset_applications,
    UpdateStatusResult,
    update_application_status
)

@pytest.fixture
def reset_state():
    reset_applications()

    yield

    reset_applications()

    
def test_add_application(reset_state):

    company = 'Google'
    position = 'Backend Developer'

    application = add_application(
        company,
        position
    )

    applications = get_all_applications()

    assert application.company == company
    assert application.position == position
    assert application.id == 1
    assert application.status == 'planned'
    assert len(applications) == 1
    assert applications[0] is application


def test_add_application_increments_id(reset_state):

    first_application = add_application(
        "Google",
        "Backend Developer",
    )

    second_application = add_application(
        "REWE",
        "Frontend Developer",
    )

    applications = get_all_applications()

    assert first_application.id == 1
    assert second_application.id == 2
    assert len(applications) == 2
    assert applications[0] is first_application
    assert applications[1] is second_application


def test_find_application_by_id_returns_application(reset_state):
    _ = add_application(
        "Google",
        "Backend Developer"
    )

    second_application = add_application(
        "REWE",
        "Frontend Developer"
    )

    result = find_application_by_id(2)

    assert result is second_application

def test_find_application_by_id_returns_none_when_not_found(reset_state):
    add_application(
        "Google",
        "Backend Developer"
    )

    result = find_application_by_id(999)

    assert result is None

def test_delete_application_removes_application(reset_state):
    first_application = add_application(
        "Google",
        "Backend Developer",
    )

    second_application = add_application(
        "REWE",
        "Frontend Developer",
    )

    result = delete_application(first_application.id)


    applications = get_all_applications()

    assert result is True
    assert len(applications) == 1
    assert applications[0] is second_application
    assert find_application_by_id(first_application.id) is None

def test_delete_application_removes_application_false_when_not_found(reset_state):
    first_application = add_application(
        "Google",
        "Backend Developer",
    )

    second_application = add_application(
        "REWE",
        "Frontend Developer",
    )

    applications_before = get_all_applications()
    length = len(applications_before)

    result = delete_application(999)

    applications_after = get_all_applications()

    assert result is False
    assert len(applications_after) == length
    assert applications_after[0] is first_application
    assert applications_after[1] is second_application

def test_update_application_status_updates_status(reset_state):
    application = add_application(
        "Google",
        "Backend Developer",
    )

    result, updated_application = update_application_status(
        application.id,
        "interview",
    )

    assert result is UpdateStatusResult.UPDATED
    assert updated_application is application
    assert updated_application.status == "interview"

def test_update_application_status_application_not_found(reset_state):
    result, updated_application = update_application_status(
        999,
        "interview",
    )

    assert result is UpdateStatusResult.APPLICATION_NOT_FOUND
    assert updated_application is None

def test_update_application_status_invalid_status(reset_state):
    application = add_application(
        "Google",
        "Backend Developer",
    )

    result, updated_application = update_application_status(
        application.id,
        "waiting",
    )

    assert result is UpdateStatusResult.INVALID_STATUS
    assert updated_application is None
    assert application.status == 'planned'