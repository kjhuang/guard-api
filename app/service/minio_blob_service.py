"""
MinIO blob service
"""

import os
import time
from queue import Empty, Queue
from threading import Thread
from typing import Any

from miniopy_async import Minio
from miniopy_async.commonconfig import CopySource
from miniopy_async.deleteobjects import DeleteObject

from app.utils import config


class MinioProgress(Thread):
    """
    handling upload progress
    """

    def __init__(self, tracker: Any):
        Thread.__init__(self)
        self.tracker = tracker

        self.daemon = True
        self.total_length = 0
        self.object_name = ""
        self.current_size = 0
        self.interval = 1
        self.display_queue = Queue()
        self.initial_time = time.time()
        self.start()

    def set_meta(self, total_length, object_name):
        """
        Metadata settings for the object. This method called before uploading object
        """
        self.total_length = total_length
        self.object_name = object_name

    def run(self):
        while True:
            try:
                # display every interval secs
                task = self.display_queue.get(timeout=self.interval)
            except Empty:
                continue

            current_size, total_length = task
            # if self.tracker:
            #     self.tracker(current_size, total_length)
            self.display_queue.task_done()

            if current_size == total_length:
                # once we have done uploading everything return
                self.done_progress()
                return

    def update(self, size):
        """
        Update object size to be showed. This method called while uploading
        """
        if isinstance(size, int):
            print("[MinioProgress] update: size=", size)
            self.current_size += size
            if self.tracker:
                self.tracker(self.current_size, self.total_length)
            self.display_queue.put((self.current_size, self.total_length))

    def done_progress(self):
        """
        progress is done
        """
        self.total_length = 0
        self.object_name = None
        self.current_size = 0


class MinioBlobService:
    """
    blob service using minio
    """

    def create_minio_client(self) -> Minio:
        """create minio client"""
        minio_end_point = f"{config.MINIO_HOST}:{config.MINIO_PORT}"
        minio_client = Minio(
            minio_end_point,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False,
        )
        return minio_client

    async def upload(
        self, file_path: str, object_name: str, file_type: str, progress=None
    ):
        minio_client = self.create_minio_client()

        is_bucket_exist = await minio_client.bucket_exists(config.BLOB_CONTAINER)
        if not is_bucket_exist:
            await minio_client.make_bucket(config.BLOB_CONTAINER)

        minio_progress = MinioProgress(progress)
        result = await minio_client.fput_object(
            config.BLOB_CONTAINER,
            object_name,
            file_path,
            content_type=file_type,
            progress=minio_progress,
        )
        print(
            f"created {result.object_name} object; etag:{result.etag}, version_id={result.version_id}"
        )

        file_size = os.stat(file_path).st_size

        upload_blob_stat = {"file_size": file_size, "file_md5": None}

        return upload_blob_stat

    async def download(self, object_name: str, file_path: str):
        minio_client = self.create_minio_client()

        await minio_client.fget_object(config.BLOB_CONTAINER, object_name, file_path)

    async def copy(self, src_object_name: str, dest_object_name: str):
        minio_client = self.create_minio_client()
        result = await minio_client.copy_object(
            config.BLOB_CONTAINER,
            dest_object_name,
            CopySource(config.BLOB_CONTAINER, src_object_name),
        )
        print(
            f"copy object; object_name:{result.object_name}, version_id:{result.version_id}"
        )
        return True

    async def delete(self, object_name: str) -> bool:
        minio_client = self.create_minio_client()
        await minio_client.remove_object(config.BLOB_CONTAINER, object_name)

    async def delete_objects(self, *object_names):
        minio_client = self.create_minio_client()
        delete_object_list = [DeleteObject(object_name) for object_name in object_names]
        errors = await minio_client.remove_objects(
            config.BLOB_CONTAINER, delete_object_list
        )
        error_count = len(errors)
        deleted_count = len(delete_object_list) - error_count
        return deleted_count
