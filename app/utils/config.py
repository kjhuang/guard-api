"""
app config
"""

import os

BLOB_URL_PREFIX = os.getenv("BLOB_URL_PREFIX")
BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")
MINIO_HOST = os.getenv("MINIO_HOST", default=None)
MINIO_PORT = os.getenv("MINIO_PORT", default=None)
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", default=None)
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", default=None)
UPLOAD_DIR = "/uploads"
