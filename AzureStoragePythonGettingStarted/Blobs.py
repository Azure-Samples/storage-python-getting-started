
import uuid
import random
import io
import os
import time

from azure.storage import CloudStorageAccount
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.storage.blob import PublicAccess

class BlobSamples():

    #declare variables
    containername = 'container1'
    blobname = "pythonqueue5"
    blobpath = "c:\\upload\\pldok.log"

    def RunAllSamples(account):

        #create a new queue service that can be passed to all methods
        block_blob_service = CloudStorageAccount.create_block_blob_service(account)

    def create_container(block_blob_service):
        block_blob_service.create_container(containername)
        block_blob_service.set_container_acl('pythoncontainer1', public_access= PublicAccess.Container)

    def create_block_blob(block_blob_service):
        block_blob_service.create_blob_from_path(containername,blobname,blobpath)

#    def list_block_blobs(
#generator = block_blob_service.list_blobs('pythoncontainer1')
#for blob in generator:
#    print(blob.name)
#block_blob_service.get_blob_to_path('pythoncontainer1','myblockblob','c:\\download\\pldok.log')
