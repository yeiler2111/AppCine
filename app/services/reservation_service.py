from typing import List
from app.redis_client import redis_instance

class ReservationService:
    def __init__(self, ttl_seconds: int = 180):
        self.redis = redis_instance.get_client()
        self.ttl = ttl_seconds

    async def reserve_seats(self, showtime_id: int, seat_ids: List[int], user_id: int):
        reserved, failed = [], []

        for seat_id in seat_ids:
            key = f"seat:{showtime_id}:{seat_id}"
            was_set = await self.redis.set(key, user_id, ex=self.ttl, nx=True)
            if was_set:
                reserved.append(seat_id)
            else:
                failed.append(seat_id)

        return {"reserved": reserved, "failed": failed, "ttl_seconds": self.ttl}

    async def release_seats(self, showtime_id: int, seat_ids: List[int], user_id: int):
        released = []
        for seat_id in seat_ids:
            key = f"seat:{showtime_id}:{seat_id}"
            current_user = await self.redis.get(key)
            if str(current_user) == str(user_id):  # Evitar liberar sillas de otro
                await self.redis.delete(key)
                released.append(seat_id)
        return {"released": released}

    async def check_availability(self, showtime_id: int, seat_id: int):
        key = f"seat:{showtime_id}:{seat_id}"
        return await self.redis.get(key) is None
