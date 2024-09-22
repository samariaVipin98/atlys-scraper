from api.auth.auth_router import router as auth_router
from api.scraper.scraper_router import router as scraper_router
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.responses import JSONResponse

api_app = FastAPI()

api_app.include_router(auth_router)
api_app.include_router(scraper_router)

app = FastAPI()

app.mount("/api", api_app)


@api_app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detail = {
        "msg": "API request not in proper format",
        "msg_code": "validation_error",
        "error_list": exc.errors(),
    }
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": detail, "success": False, "data": {}}),
    )


@api_app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail, "success": False, "data": {}}),
    )
