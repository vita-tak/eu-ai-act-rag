from fastapi import Depends, FastAPI
from src.api.router import router
from src.middleware.security import rate_limit, register_security

app = FastAPI()
register_security(app)
app.include_router(router, dependencies=[Depends(rate_limit)])
