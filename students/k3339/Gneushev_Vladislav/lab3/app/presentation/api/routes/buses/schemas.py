from pydantic import BaseModel


class GetBusTypeSchema(BaseModel):
    id: int
    name: str
    people_capacity: int


class AddBusTypeSchema(BaseModel):
    name: str
    people_capacity: int


class GetBusSchema(BaseModel):
    id: int
    bus_type: GetBusTypeSchema
    state_number: str


class AddBusSchema(BaseModel):
    state_number: str
    bus_type_id: int

