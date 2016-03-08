class QueueStorage(object):
    """description of class"""
   
import uuid
import random
import io
import os
import time

from azure.storage import CloudStorageAccount
from azure.storage.queue import QueueService
from azure.storage.blob import ContentSettings
from azure.storage.blob import PublicAccess

queueName = "PythonQueue"
messageName = "Test message"

queue_service = QueueService(account_name = "devstoreaccount1", account_key = "")
queue_service.create_queue("PythonQueue")
queue_service.put_message(str, 