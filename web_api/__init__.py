from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from web_api.endpoint import router


app = FastAPI(
    title="Test Task Secunda",
    description="Backend API for Test Task Secunda",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router, prefix="/api", tags=["test endpoints"])
