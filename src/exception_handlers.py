from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse, HTMLResponse
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


# async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> HTMLResponse:
#     return HTMLResponse(
#         content=f"""
#         <h1>422</h1></br>
#         {'</br>'.join(f'<h2>{e.get("msg")}</h2>' for e in exc.errors())}
#         """
#     )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": jsonable_encoder(
                obj=exc.errors(),
                exclude={"url", "type", "loc", "ctx"}
            )
        },
    )
