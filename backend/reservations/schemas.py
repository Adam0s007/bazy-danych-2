from pydantic import BaseModel

from dependencies import FromMongoDB


class ReservationBasic(BaseModel):
    client_id: int
    train_id: str
    seat: int


class Reservation(ReservationBasic):
    reservation_time: int


class ReservationDb(FromMongoDB, Reservation):
    # Can read MongoDb ObjectID type as string
    pass
