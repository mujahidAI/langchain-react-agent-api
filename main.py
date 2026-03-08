from fastapi import FastAPI
from routers.agents import router as agents_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Agent API",
)
app.include_router(agents_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
async def health():
    return {"status": "ok"}
