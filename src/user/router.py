from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import select
from starlette.requests import Request
from starlette.responses import Response

from core.database.database import database
from core.model.admin_model import AuthType, VdManager, VmPartType

router = APIRouter()


class TestUser(BaseModel):
    id: int = Field(...)
    email: str = Field(...)
    auth_id: int = Field(...)
    name: str = Field(...)
    phone: str = Field(...)
    is_active: bool = Field(...)
    department_id: int = Field(...)
    part_id: int = Field(...)
    position_id: int = Field(...)


@router.get("", response_model=List[TestUser])
async def test(request: Request, response: Response):

    query = (
        select(
            VdManager.id,
            VdManager.name,
            VdManager.phone,
            VdManager.auth_id,
            VdManager.part_id,
            VdManager.department_id,
            VdManager.email,
            VdManager.position_id,
            VdManager.is_active,
            VmPartType.__table__.columns,
            AuthType.__table__.columns,
        )
        .join_from(VdManager, VmPartType, VdManager.part_id == VmPartType.id)
        .join_from(VdManager, AuthType, VdManager.auth_id == AuthType.id)
    )

    result = await database.fetch_join_all('SYSTEM', query)
    return result
