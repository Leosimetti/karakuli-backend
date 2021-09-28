from fastapi import APIRouter

api = APIRouter(tags=["Auth"], prefix="/auth")

for name in ["common", "cookie", "jwt"]:
    package = __import__("app.routers.auth." + name, fromlist=["api"])
    package_api = getattr(package, "api")
    api.include_router(package_api)

