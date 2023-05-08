from dependencies import FromMongoDB


class TrainDb(FromMongoDB):
    name: str
    free_seats: list[int]
