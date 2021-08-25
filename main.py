import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=os.getenv("HOST_IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        reload=True,
    )
