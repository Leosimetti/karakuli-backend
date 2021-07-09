from app.routers.auth import api
from app import app

prefix = "/api"

app.include_router(api, prefix=prefix)
# app.include_router(dashboard_router, prefix=f"{prefix}")
# app.include_router(words_router, prefix=f"{prefix}/words")
# app.include_router(reviews_router, prefix=f"{prefix}/reviews")
