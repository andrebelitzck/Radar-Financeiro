from fastapi import APIRouter, Query
from app.schemas import HealthResponse

router = APIRouter(tags=['health'])


@router.get('/health', response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()
