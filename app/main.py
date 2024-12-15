"""
app main
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_route import router as auth_router
from app.routes.item_route import router as item_router
from app.routes.order_route import router as order_router

app = FastAPI(title="guard api", description="guard api doc", version="0.0.0")


# set cors
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(item_router)
app.include_router(order_router)
