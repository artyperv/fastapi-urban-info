import uuid
from pydantic import BaseModel, Field, constr


# --- Building ---
class BuildingBase(BaseModel):
    address: str = Field(..., min_length=1, max_length=255)
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
