from fastapi import APIRouter, FastAPI

from ersms_test.api.events.router import events_router

app = FastAPI(
    title="PlayPal events REST API",
    description="PlayPal events REST API",
    version='0.0.1',
    docs_url="/api/ui",
)

api_router = APIRouter(prefix='/api')
api_router.include_router(events_router)

app.include_router(api_router)
