from app.services import (
    add_application,
    delete_application,
    find_application_by_id,
)


def test_add_application_saves_to_database(db_session):
    application = add_application(
        db_session,
        "Google",
        "Backend Developer",
    )

    assert application.id == 1

    saved_application = find_application_by_id(
        db_session,
        application.id,
    )

    assert saved_application is application

def test_find_application_by_id_returns_none(
    db_session,
):
    result = find_application_by_id(
        db_session,
        999,
    )

    assert result is None


def test_delete_application_removes_from_database(
    db_session,
):
    application = add_application(
        db_session,
        "Google",
        "Backend Developer",
    )

    result = delete_application(
        db_session,
        application.id,
    )

    assert result is True
    assert (
        find_application_by_id(
            db_session,
            application.id,
        )
        is None
    )