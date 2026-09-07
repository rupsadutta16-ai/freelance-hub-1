import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


from app.core.config import settings
from app.db.database import Base, engine

logger = logging.getLogger("unigigs")


from app.routers import (
    auth,
    users,
    gig,
    application,
    contracts,
    messages,
    reviews,
    notifications,  # ✅ ADDED
)

app = FastAPI(
    title="UniGigs API",
    description="Student-focused freelance/gig marketplace API",
    version="1.0.0",
    debug=False,
)


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.exception(
        "Unhandled exception: path=%s method=%s",
        request.url.path,
        request.method,
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "path": request.url.path,
        },
    )


# CORS
cors_origins = settings.cors_origins_list

if "*" in cors_origins:
    # Allow all origins explicitly.
    allow_origins = ["*"]
    allow_origin_regex = None
else:
    allow_origins = cors_origins
    allow_origin_regex = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)


app.include_router(
    users.router,
    prefix="/api/users",
    tags=["Users"]
)


app.include_router(
    gig.router,
    prefix="/api/gigs",
    tags=["Gigs"]
)


app.include_router(
    application.router,
    prefix="/api/applications",
    tags=["Applications"]
)


app.include_router(
    contracts.router,
    prefix="/api/contracts",
    tags=["Contracts"]
)


app.include_router(
    messages.router,
    prefix="/api/messages",
    tags=["Messages"]
)


app.include_router(
    reviews.router,
    prefix="/api/reviews",
    tags=["Reviews"]
)


app.include_router(
    notifications.router,
    prefix="/api/notifications",
    tags=["Notifications"]  # ✅ ADDED
)


@app.get("/")
def root():
    return {
        "message": "Welcome to UniGigs API",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}