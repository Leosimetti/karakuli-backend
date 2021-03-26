import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run("app:app", host=os.getenv("HOST_IP", "localhost"), port=5000)
