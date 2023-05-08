from typing import Optional

from fastapi import APIRouter

from dependencies import db

router = APIRouter(
    prefix="/trains"
)
trains_collection = db["trains"]


def add_example_trains(seats_num: int, trains_names: Optional[list[str]] = None):
    if trains_names is None:
        trains_names = ['Wawel', 'Mehoffer', 'Malczewski', "Łokietek"]
    new_trains = []
    for name in trains_names:
        new_trains.append({'name': name, 'free_seats': [1 for _ in range(seats_num)]})
    trains_collection.insert_many(new_trains)


@router.get("/")
def list_trains():
    return list(trains_collection.find({}))
