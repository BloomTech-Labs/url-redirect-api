from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import MongoDB


API = FastAPI(
    title="BloomTech Labs URL Redirect API",
    version="0.0.1",
    docs_url="/",
)
API.db = MongoDB()
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@API.get("/version")
async def api_version():
    """ Returns current API version
    @return: String Version """
    return API.version

