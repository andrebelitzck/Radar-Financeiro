from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.database import init_db
from app.routes.health import router as health_router
from app.routes.sync import router as sync_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title='Radar Financeiro Backend', version='0.1.0', lifespan=lifespan)
app.include_router(health_router)
app.include_router(sync_router)

if ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@app.get('/')
def root() -> dict[str, str]:
    return {'message': 'Radar Financeiro Backend OK'}
