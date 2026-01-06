import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, Request, HTTPException, status
from sqlalchemy.engine.base import Engine
from sqlmodel import Session

from vsm_restaurant.db import run_migrations, create_db_engine
from vsm_restaurant.settings import Settings

logger = logging.getLogger(__name__)

settings = Settings()


def get_settings(request: Request):
    return request.app.state.settings


def get_engine(request: Request):
    return request.app.state.engine


def get_session(engine: Engine = Depends(get_engine)):
    with Session(engine) as session:
        yield session



SessionDep = Annotated[Session, Depends(get_session)]


def require_admin_token(
    request: Request,
    settings: Settings = Depends(get_settings),
):
    """Protect admin endpoints with a static token in Authorization header.

    Supported formats:
      - Authorization: Bearer <token>
      - Authorization: <token>
    """
    raw = request.headers.get("Authorization")
    if not raw:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")

    token = raw
    if raw.lower().startswith("bearer "):
        token = raw[7:].strip()

    if not token or token != settings.admin_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings

    run_migrations(settings)

    engine = create_db_engine(settings)
    app.state.engine = engine

    yield # Wait until the app shuts down

    # Here we can do some post-shutdown tasks, but there is nothing to do for now.
