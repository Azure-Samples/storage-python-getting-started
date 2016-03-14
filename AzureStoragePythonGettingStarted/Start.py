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

#---------------------------------------------------------------------------
#This sample can be run using either the Azure Storage Emulator (Windows) or by updating the config.properties file with your Storage account name and key.

#To run the sample using the Storage Emulator (default option):
#1.Download and install the Azure Storage Emulator https://azure.microsoft.com/en-us/downloads/ 
#2.Start the emulator (once only) by pressing the Start button or the Windows key and searching for it by typing "Azure Storage Emulator". Select it from the list of applications to start it.
#3.Set breakpoints and run the project. 

#To run the sample using the Storage Service
#1.Open the config.properties file and comment out the connection string for the emulator (UseDevelopmentStorage=True) and uncomment the connection string for the storage service (AccountName=[]...).
#2.Create a Storage Account through the Azure Portal and provide your [AccountName] and [AccountKey] in the config.properties file. See https://azure.microsoft.com/en-us/documentation/articles/storage-create-storage-account/ for more information
#3.Set breakpoints and run the project. 
#---------------------------------------------------------------------------

from azure.storage import CloudStorageAccount
import config
import Queues

print('Azure Storage samples for Python')

# Create the storage account object and specify its credentials to either point to the local Emulator or your Azure subscription
if config.IS_EMULATED:
    account = CloudStorageAccount(is_emulated=True)
else:
    account_name = config.STORAGE_ACCOUNT_NAME
    account_key = config.STORAGE_ACCOUNT_KEY

    try:
        account = CloudStorageAccount(account_name, account_key, is_emulated=False)
    except Exception as e:
        print ('Account name and key cannot be empty')

##Basic Blob samples
#print('Azure Storage Blob samples')
##Blobs.BlobSamples.RunAllSamples(account)

##Basic File samples
#print('Azure Storage File samples')
##File.FileSamples.RunAllSamples(account)

##Basic Table samples
#print('Azure Storage Table samples')
##Table.TableSamples.RunAllSamples(account)

#Basic Queue samples
print('Azure Storage Queue samples')
Queues.QueueSamples.RunSamples(account)

