from pydantic import BaseModel, ConfigDict, Field

class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    position: str = Field(min_length=1, max_length=100)

class ApplicationStatusUpdate(BaseModel):
    status: str = Field(min_length=1)

class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    position: str
    status: str