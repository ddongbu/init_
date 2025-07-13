from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import select
from starlette.requests import Request
from starlette.responses import Response

from core.database.database import database
from core.model.admin_model import AuthType, VdManager, VmPartType

router = APIRouter()
