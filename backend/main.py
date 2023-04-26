import time
import uuid

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from models import ReservationRequest, TrainDb, ReservationDatabase, ReservationMake

app = FastAPI()

# Configure CORS middleware
origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cluster = MongoClient("mongodb+srv://user-1:x7WQrVTGeNXBEnM1@cluster0.hvrxxdq.mongodb.net/?retryWrites=true&w=majority")
db = cluster["main-database"]
collection = db["collection"]
trains_collection = db["trains"]
reservations_collection = db["reservations"]


def key() -> str:
    return str(uuid.uuid4().int & (1 << 64) - 1)


def example_trains():
    trains = [
        {'name': 'Mehoffer', '_id': key(), 'free_seats': [1 for _ in range(20)]},
        {'name': 'Wawel', '_id': key(), 'free_seats': [1 for _ in range(20)]},
        {'name': 'Malczewski', '_id': key(), 'free_seats': [1 for _ in range(20)]}
    ]
    response = trains_collection.insert_many(trains)


# example_trains()

@app.get("/trains")
def list_trains():
    return list(trains_collection.find({}))


@app.get("/reservation/details")
def list_trains(train_id: str, seat_id: int):
    data = reservations_collection.find_one({"train_id": train_id, "seat": seat_id})
    reservation: ReservationDatabase = ReservationDatabase.parse_obj(data)
    return reservation


@app.get("/delete")
def reservation_delete(train_id: str, seat_id: int):
    print("DELETE " + train_id + " " + str(seat_id))
    reservations_collection.delete_one({"train_id": train_id, "seat": seat_id})
    train: dict = trains_collection.find_one({"_id": train_id})
    train: TrainDb = TrainDb.parse_obj(train)
    print(train)
    updated_seats: list[int] = train.free_seats
    updated_seats[seat_id] = 1
    trains_collection.update_one({'_id': train.id}, {'$set': {'free_seats': updated_seats}})


@app.post("/reservation")
def add_reservation(reservation: ReservationRequest):
    train: dict = trains_collection.find_one({"_id": reservation.train_id})
    print(train)
    train: TrainDb = TrainDb.parse_obj(train)
    print(train)
    if train is None:
        print("CAN NOT FIND TRAIN.")
        raise HTTPException(status_code=404, detail="Item not found")
    if reservation.seat <= len(train.free_seats) and bool(train.free_seats[reservation.seat]):
        new_reservation = ReservationMake(_id=key(),
                                          full_name=reservation.full_name,
                                          train_id=reservation.train_id,
                                          seat=reservation.seat,
                                          reservation_time=int(time.time())
                                          )

        reservations_collection.insert_one(new_reservation.dict())
        updated_seats: list[int] = train.free_seats
        updated_seats[reservation.seat] = 0
        trains_collection.update_one({'_id': train.id}, {'$set': {'free_seats': updated_seats}})
        print("Dodano rezerwacje")
    else:
        raise HTTPException(status_code=404, detail="Seat number invalid or taken")


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
def shutdown_event():
    cluster.close()

# @app.get("/trains", response_description="List all trains", response_model=List[Train])
# def list_books(request: Request):
#     books = list(request.app.database["books"].find(limit=100))
#     return books
