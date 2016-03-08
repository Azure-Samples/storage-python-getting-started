#-------------------------------------------------------------------------
# Copyright (c) Microsoft.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#--------------------------------------------------------------------------

import uuid
import random
import io
import os
import time

from azure.storage import CloudStorageAccount
from azure.storage.queue import QueueService
from azure.storage.queue import Queue
from azure.storage.queue import QueueMessage
import config

class QueueSamples():

    
    def RunAllSamples(account):

        #declare variables
        queuename = "pythonqueue4"
        messagename = "test message"

        #create a new queue service that can be passed to all methods
        queue_service = CloudStorageAccount.create_queue_service(account)

        #create a new queue
        QueueSamples.create_queue(queue_service, queuename)
        QueueSamples.add_message(queue_service, queuename, messagename)
        QueueSamples.peek_message(queue_service, queuename)
        QueueSamples.list_queues(queue_service)

    def create_queue(queue_service, queuename):  
        # Create a queue or leverage one if already exists
        queue_service.create_queue(queuename, fail_on_exist=False)

    def add_message(queue_service, queuename, messagename):
        # Add a message to the queue
        queue_service.put_message(queuename, messagename)

    def peek_message(queue_service, queuename):
        metadata = queue_service.get_queue_metadata(queuename)
        length = metadata.approximate_message_count
        print(length)
        #Look at the contents of all messages
        messages = queue_service.peek_messages(queuename)
        for message in messages:
            print(message.content)
        messages = queue_service.get_messages(queuename, num_messages=2)
        for message in messages:
            print(message.content) # message1, message2

    def list_queues(queue_service):
        queues = list(queue_service.list_queues())
        for queue in queues:
            print(queue.name) # queue1, queue2, or whichever 2 queues are alphabetically first in your account
