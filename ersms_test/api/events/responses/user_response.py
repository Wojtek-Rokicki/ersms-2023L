from ersms_test.database.models import User
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    login: str

    @classmethod
    def from_database_object(cls, user: User):
        return cls(
            id=user.id,
            login=user.login
        )
