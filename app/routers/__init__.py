from app.routers.auth import api as auth_api
from app.routers.review import api as review_api
from app.routers.study import api as study_api
from app.routers.word import api as word_api
from app import app

prefix = "/api"

app.include_router(auth_api)
app.include_router(review_api)
app.include_router(word_api)
app.include_router(study_api)
# app.include_router(dashboard_router, prefix=f"{prefix}")
# app.include_router(words_router, prefix=f"{prefix}/words")
