from app.services import(
    ALLOWED_STATUSES,
    UpdateStatusResult,
    add_application,
    delete_application,
    find_application_by_id,
    find_application_by_company,
    get_all_applications,
    update_application_status
)

def show_menu():
    print("\nJob Application Tracker")
    print("1. Add application")
    print("2. Show all applications")
    print("3. Find application by ID")
    print("4. Update application status")
    print("5. Delete application")
    print("6. Search applications by company")
    print("0. Exit")

def handle_add_application():
    company = input("Enter company name: ").strip()
    position = input("Enter position: ").strip()

    if not company or not position:
        print("Company and position cannot be empty.")
        return

    application = add_application(company, position)
    print("Application added:")
    print(application)

def handle_show_all_applications():
    applications = get_all_applications()

    if not applications:
        print("No applications found.")
        return

    for application in applications:
        print(application)

def handle_find_application_by_id():
    try:
        application_id = int(input("Enter application ID: "))
    except ValueError:
        print("ID must be a number")
        return

    application = find_application_by_id(application_id)

    if application is None:
        print("Application not found.")
        return

    print(application)

def handle_update_application_status():
    try:
        application_id = int(input("Enter application ID: "))
    except ValueError:
        print("ID must be a number.")
        return

    print("Allowed statuses:")
    print(", ".join(sorted(ALLOWED_STATUSES)))

    new_status = input("Enter new status: ").strip().lower()

    result, application = update_application_status(
        application_id,
        new_status,
    )

    if result == UpdateStatusResult.INVALID_STATUS:
        print("Invalid status.")
        print(
            "Allowed statuses: "
            + ", ".join(sorted(ALLOWED_STATUSES))
        )
        return

    if result == UpdateStatusResult.APPLICATION_NOT_FOUND:
        print("Application not found.")
        return

    print("Application status updated.")
    print(application)

def handle_delete_application():
    try:
        application_id = int(input("Enter application ID: "))
    except ValueError:
        print("ID must be a number.")
        return

    deleted = delete_application(application_id)

    if not deleted:
        print("Application not found.")
        return

    print("Application deleted.")

def handle_search_by_company():
    company_name = input("Enter company name: ").strip()

    if not company_name:
        print("Company name cannot be empty.")
        return

    results = find_application_by_company(company_name)

    if not results:
        print("Application not found.")
        return

    for application in results:
        print(application)

def run_menu():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_add_application()
        elif choice == "2":
            handle_show_all_applications()
        elif choice == "3":
            handle_find_application_by_id()
        elif choice == "4":
            handle_update_application_status()
        elif choice == "5":
            handle_delete_application()
        elif choice == "6":
            handle_search_by_company()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")