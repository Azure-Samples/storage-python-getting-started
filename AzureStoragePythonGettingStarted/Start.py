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
import config
import Tables
import Queues

# Create a queue service object
if config.IS_EMULATED:
    account = CloudStorageAccount(is_emulated=True)
else:
    account_name = config.STORAGE_ACCOUNT_NAME
    account_key = config.STORAGE_ACCOUNT_KEY
    sas = config.SAS
    account = CloudStorageAccount(account_name, account_key)

#Basic Blob samples
#Blobs.BlobSamples.RunAllSamples(account)

#Basic File samples

#Basic Table samples
Tables.TableSamples.RunAllSamples(account)

#Basic Queue samples
Queues.QueueSamples.RunAllSamples(account)

