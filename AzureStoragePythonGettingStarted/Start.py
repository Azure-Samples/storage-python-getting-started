#-------------------------------------------------------------------------
# Microsoft Developer & Platform Evangelism
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, 
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
#----------------------------------------------------------------------------------
# The example companies, organizations, products, domain names,
# e-mail addresses, logos, people, places, and events depicted
# herein are fictitious. No association with any real company,
# organization, product, domain name, email address, logo, person,
# places, or events is intended or should be inferred.
#--------------------------------------------------------------------------

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

import config
import azure.common
from azure.storage import CloudStorageAccount
from Queues import queue_samples
from Tables import table_samples
from Files import file_samples
from Blobs import blob_samples

print('Azure Storage samples for Python')

#try:
    # Create the storage account object and specify its credentials to either point to the local Emulator or your Azure subscription
if config.IS_EMULATED:
    account = CloudStorageAccount(is_emulated=True)
else:
    account_name = config.STORAGE_ACCOUNT_NAME
    account_key = config.STORAGE_ACCOUNT_KEY
    account = CloudStorageAccount(account_name, account_key)

#Basic Blob samples
print ('---------------------------------------------------------------')
print('Azure Storage Blob samples')
blob_samples.run_all_samples(account)

#Basic File samples
print ('---------------------------------------------------------------')
print('Azure Storage File samples')
file_samples.run_all_samples(account)

#Basic Table samples
print ('---------------------------------------------------------------')
print('Azure Storage Table samples')
table_samples.run_all_samples(account)

#Basic Queue samples
print ('---------------------------------------------------------------')
print('Azure Storage Queue samples')
queue_samples.run_all_samples(account)
