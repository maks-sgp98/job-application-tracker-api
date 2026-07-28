class JobApplication:
    def __init__(
        self,
        application_id,
        company,
        position,
        status='planned'
    ):
        self.id = application_id
        self.company = company
        self.position = position
        self.status = status

    def __str__(self):
        return (
            f"ID: {self.id} | "
            f"Company: {self.company} | "
            f"Position: {self.position} | "
            f"Status: {self.status}" 
        )