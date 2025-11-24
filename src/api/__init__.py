from fastapi import FastAPI, Response, APIRouter

app = FastAPI()

v1_router = APIRouter(prefix="/api/v1")

@v1_router.get('/status/checkhealth')
async def checkhealth() -> Response:
    """
    Returns a simple 200 health response.
    """
    return Response()

app.include_router(v1_router)



