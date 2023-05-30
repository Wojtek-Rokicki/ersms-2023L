from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ersms_test.database import db_session_get
from ersms_test.database.models import User
from .responses import UserResponse

events_router = APIRouter(prefix='/events')


@events_router.get(
	"",
	responses={
		200: {
			"model": list[UserResponse],
			"description": "Successfully read nothing"
		}
	},
	tags=["Events"],
	summary="Test",
)
async def api_endpoints_events_get_nothing() -> JSONResponse:
	with db_session_get() as db_session:
		users = db_session.query(User).all()
	return JSONResponse(content=[UserResponse.from_database_object(user) for user in users], status_code=200)
