from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from dependencies import db, client
from reservations.schemas import *
from trains.schemas import TrainDb

router = APIRouter(
    prefix="/reservations"
)

reservations_collection = db["reservations"]
trains_collection = db["trains"]


@router.post("/make")
def make_reservation(request: ReservationBasic):
    print(request)
    with client.start_session() as session:
        with session.start_transaction():
            train = trains_collection.find_one({"_id": ObjectId(request.train_id)}, session=session)
            if train is None:
                raise HTTPException(status_code=404, detail="Train not found")
            train = TrainDb.parse_obj(train)

            seat_taken: bool = train.free_seats[request.seat] == 0
            if seat_taken:
                raise HTTPException(status_code=404, detail="Seat number invalid or taken")

            reservation = Reservation(
                client_id=request.client_id,
                train_id=train.id,
                seat=request.seat,
                reservation_time=int(datetime.now().timestamp())
            )

            reservations_collection.insert_one(reservation.dict(), session=session)

            updated_seats: list[int] = train.free_seats
            updated_seats[request.seat] = 0
            trains_collection.update_one({'_id': ObjectId(train.id)}, {'$set': {'free_seats': updated_seats}},
                                         session=session)


@router.get("/details")
def reservation_details(train_id: str, seat_id: int):
    db_reservation = reservations_collection.find_one({"train_id": train_id, "seat": seat_id})
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    reservation = ReservationDb.parse_obj(db_reservation)
    return reservation


@router.delete("/delete")
def reservation_delete(train_id: str, seat_id: int):
    reservations_collection.delete_one({"train_id": train_id, "seat": seat_id})
    train: dict = trains_collection.find_one({"_id": train_id})
    train: TrainDb = TrainDb.parse_obj(train)
    updated_seats: list[int] = train.free_seats
    updated_seats[seat_id] = 1
    trains_collection.update_one({'_id': train.id}, {'$set': {'free_seats': updated_seats}})
