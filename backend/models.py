from pydantic import BaseModel, Field


class ReservationRequest(BaseModel):
    full_name: str
    train_id: str
    seat: int


class ReservationOut(BaseModel):
    id: str = Field(alias='_id')
    full_name: str
    train_id: str
    seat: int


class ReservationDatabase(BaseModel):
    id: str
    full_name: str
    train_id: str
    seat: int
    reservation_time: int


class ReservationMake(BaseModel):
    id: str = Field(alias='_id')
    full_name: str
    train_id: str
    seat: int
    reservation_time: int


class TrainDb(BaseModel):
    id: str = Field(alias='_id')
    name: str
    free_seats: list[int]
