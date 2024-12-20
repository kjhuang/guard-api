"""
app main
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.utils.config as config
from app.routes.announce_route import router as announce_router
from app.routes.auth_route import router as auth_router
from app.routes.repair_order_route import router as repair_order_router

# from app.routes.item_route import router as item_router
# from app.routes.order_route import router as order_router
from app.routes.site_route import router as site_router
from app.routes.value_route import router as value_router
from app.routes.buidling_route import router as building_router

app = FastAPI(title="guard api", description="guard api doc", version="0.0.2")

# Ensure upload dir exists
os.makedirs(config.UPLOAD_DIR, exist_ok=True)

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
app.include_router(site_router)
app.include_router(building_router)
app.include_router(announce_router)
app.include_router(repair_order_router)
app.include_router(value_router)
# app.include_router(item_router)
# app.include_router(order_router)
