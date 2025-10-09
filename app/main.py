from fastapi import FastAPI
from app.controllers import movie_controller, payment_controller, room_controller, seat_controller, showtime_controller, user_controller, ticket_controller, reservation_controller, auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.core import config


app = FastAPI(
    title="Cine API",
    description="API para gestionar películas, salas, reservas y pagos",
    version="1.0.0"
)

app.include_router(movie_controller.router)
app.include_router(payment_controller.router)
app.include_router(room_controller.router)
app.include_router(seat_controller.router)
app.include_router(showtime_controller.router)
app.include_router(user_controller.router)
app.include_router(ticket_controller.router)
app.include_router(reservation_controller.router)
app.include_router(auth_router.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)