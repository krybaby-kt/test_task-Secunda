from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Test Task Secunda",
    description="Backend API for Test Task Secunda",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
