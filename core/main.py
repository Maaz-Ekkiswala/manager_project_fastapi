import logging
import os
import uuid
from contextvars import ContextVar

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT

from starlette.responses import JSONResponse
from starlette.routing import Match
from starlette.staticfiles import StaticFiles

from apps import api_router
from core.config import settings, Settings
from core.database import init
from core.logs import setup_logging
from core.redis_conn import redis_conn

try:
    from manager_project_fastapi.version import __version__
except ImportError:
    __version__ = "1.0.0"


logger = logging.getLogger(__name__)

def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        version=__version__,
        debug=settings.DEBUG
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


app = get_application()
request_id_contextvar = ContextVar("request_id", default=None)

static_path = os.path.join(f"{settings.STATIC_PATH}/static")
if not os.path.exists(static_path):
    os.makedirs(static_path)
media_path = os.path.join(f"{settings.MEDIA_PATH}/media")
if not os.path.exists(media_path):
    os.makedirs(media_path)

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/media", StaticFiles(directory=media_path), name="media")

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    init(app)
    setup_logging()


@app.middleware("http")
async def request_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    request_url = str(request.url)
    request_id_contextvar.set(request_id)
    request_method = request.method
    logger.info(f"Request started, Method:{request_method}, URL: {request_url}")
    routes = request.app.router.routes
    # for route in routes:
    #     match, scope = route.matches(request)
    #     if match == Match.FULL:
    #         for name, value in scope["path_params"].items():
    #             logger.debug(f"\t{name}: {value}")
    # logger.debug("Request Headers:")
    # for name, value in request.headers.items():
    #     logger.debug(f"\t{name}: {value}")
    try:
        return await call_next(request)

    except Exception as ex:
        logger.error(f"Request failed: {ex}")
        return JSONResponse(content={"success": False}, status_code=500)

    finally:
        logger.info(f"Request ended, Method:{request_method}, URL: {request_url}")


@AuthJWT.load_config
def get_config():
    return Settings()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_conn.get(jti)
    return entry and entry == 'true'