from app.routers.auth import api as auth_api
from app.routers.review import api as review_api
from app.routers.study import api as study_api
from app.routers.lessons import api as lessons_api
from app.routers.lists import api as list_api
from app import app

prefix = "/api"

app.include_router(auth_api)
app.include_router(review_api)
app.include_router(lessons_api)
app.include_router(study_api)
app.include_router(list_api)
# app.include_router(dashboard_router, prefix=f"{prefix}")
# app.include_router(words_router, prefix=f"{prefix}/words")
