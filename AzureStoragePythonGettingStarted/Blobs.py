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
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.storage.blob import PublicAccess

block_blob_service = BlockBlobService(is_emulated=True)
block_blob_service.create_container('pythoncontainer1')
block_blob_service.set_container_acl('pythoncontainer1', public_access= PublicAccess.Container)
block_blob_service.create_blob_from_path(
    'pythoncontainer1',
    'myblockblob',
    'c:\\upload\\pldok.log' 
            )
generator = block_blob_service.list_blobs('pythoncontainer1')
for blob in generator:
    print(blob.name)
block_blob_service.get_blob_to_path('pythoncontainer1','myblockblob','c:\\download\\pldok.log')
