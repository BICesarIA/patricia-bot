from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database.postgres import lifespan
from routes.twilio import router as twilio_router

app = FastAPI(lifespan=lifespan)

app.include_router(twilio_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=10000, reload=True)
