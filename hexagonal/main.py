import os
import uvicorn
from config.factory import build_app

# создаём приложение через DI-фабрику
app = build_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)
