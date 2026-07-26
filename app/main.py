applications = []
next_application_id = 1
def show_menu():
    print("\nJob Application Tracker")
    print("1. Add application")
    print("2. Show all applications")
    print("3. Find application by ID")
    print("4. Update application status")
    print("5. Delete application")
    print("6. Search applications by company")
    print("0. Exit")

def add_application():
    company = input("Company name: ").strip()
    position = input("Position: ").strip()

    if not company or not position:
        print("Company and position cannot be empty")
        return


    global next_application_id

    application = {
        "id": next_application_id,
        "company": company,
        "position": position,
        "status": "planned"
    }

    applications.append(application)
    next_application_id+=1

    print("Application added successfully.")

def show_all_applications():
    if not applications:
        print("No applications found.")
        return

    print("\nApplications:")

    for application in applications:
        print(
            f"ID: {application['id']} | "
            f"Company: {application['company']} | "
            f"Position: {application['position']} | "
            f"Status: {application['status']}"
        )

def find_application_by_id(application_id):
    for application in applications:
        if application["id"] == application_id:
            return application

    return None

def find_application_by_company(company_name):
    result = []
    for application in applications:
        if company_name in application["company"].lower():
            result.append(application)
    return result

def search_application_by_company():

    company_name = input("Enter company name: ").strip().lower()

    if not company_name:
        print("Company name connot be empty.")
        return


    result = find_application_by_company(company_name)

    if not result:
        print("Company not found.")
        return


    for application in result:
        print(
            f"ID: {application['id']} | "
            f"Company: {application['company']} | "
            f"Position: {application['position']} | "
            f"Status: {application['status']}"
        )
    
def show_application_by_id():
    try:
        application_id = int(input("Enter application ID: "))
    except ValueError:
        print("ID must be a number.")
        return

    application = find_application_by_id(application_id)

    if application is None:
        print("Application not found.")
        return

    print(
        f"ID: {application['id']} | "
        f"Company: {application['company']} | "
        f"Position: {application['position']} | "
        f"Status: {application['status']}"
    )


def update_application_status():
    try:
        application_id = int(input("Enter application ID: "))
    except ValueError:
        print("ID must be a number.")
        return

    application = find_application_by_id(application_id)

    if application is None:
        print("Application not found.")
        return

    print("Available statuses:")
    print("planned")
    print("applied")
    print("interview")
    print("offer")
    print("rejected")

    new_status = input("Enter new status ").strip().lower()

    allowed_statuses = [
        "planned",
        "applied",
        "interview",
        "offer",
        "rejected"
    ]

    if new_status not in allowed_statuses:
        print("Invalid status.")
        return

    application["status"] = new_status
    print("Application status updated.")

def delete_application():
    try:
        application_id = int(input("Enter application ID: "))
    except ValueError:
        print("ID must be a number.")
        return

    application = find_application_by_id(application_id)

    if application is None:
        print("Application not found.")
        return

    applications.remove(application)
    print("Application deleted.")

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_application()
        elif choice == "2":
            show_all_applications()
        elif choice == "3":
            show_application_by_id()
        elif choice == "4":
            update_application_status()
        elif choice == "5":
            delete_application()
        elif choice == "6":
            search_application_by_company()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()