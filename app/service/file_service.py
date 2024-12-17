"""
file service
"""

import os
import uuid
from mimetypes import MimeTypes

from fastapi import UploadFile

import app.utils.config as config
from app.service.minio_blob_service import MinioBlobService


def save_upload_file(upload_file: UploadFile):
    ori_filename = upload_file.filename
    temp_file_name = f"{uuid.uuid4().hex}_{ori_filename}"
    temp_file_path = os.path.join(config.UPLOAD_DIR, temp_file_name)
    with open(temp_file_path, "wb") as f:
        f.write(upload_file.file.read())

    return temp_file_path


async def create_from_local(
    local_file_path: str, ori_filename: str, module_name: str
) -> str:
    file_id = str(uuid.uuid4())
    _, file_ext = os.path.splitext(local_file_path)
    object_name = f"/{module_name}/{file_id}{file_ext}"
    mime = MimeTypes()
    mime_type = mime.guess_type(ori_filename)[0] or ""

    minio_blob_service = MinioBlobService()
    await minio_blob_service.upload(local_file_path, object_name, mime_type)

    return object_name


async def create_from_upload(upload_file: UploadFile, module_name: str) -> str:
    ori_filename = upload_file.filename

    temp_file_path = save_upload_file(upload_file)

    object_name = await create_from_local(temp_file_path, ori_filename, module_name)

    os.remove(temp_file_path)

    return object_name


async def delete_blob(object_name: str):
    if not object_name:
        return

    minio_blob_service = MinioBlobService()
    await minio_blob_service.delete(object_name)
