# storage-python-getting-started
Samples documenting basic operations with Azure storage services (Blob, File, Table, Queue) in Python. 

## Running this sample
This sample can be run using either the Azure Storage Emulator (Windows) or by using your Azure Storage account name and key. Please update the config.py file with the appropriate properties.

To run the sample using the Storage Emulator:
1. Download and install the Azure Storage Emulator https://azure.microsoft.com/en-us/downloads/ 
2. Start the emulator (once only) by pressing the Start button or the Windows key and searching for it by typing "Azure Storage Emulator". Select it from the list of applications to start it.
3. Run the project. 

To run the sample using the Storage Service
1. Open the config.py file and comment out the connection string for the emulator (UseDevelopmentStorage=True) and uncomment the connection string for the storage service (AccountName=[]...).
2. Create a Storage Account through the Azure Portal and provide your [AccountName] and [AccountKey] in the config.properties file. See https://azure.microsoft.com/en-us/documentation/articles/storage-create-storage-account/ for more information
3.Set breakpoints and run the project. 

## Deploy this sample 

Either fork the sample to a local folder or download the zip file from https://github.com/Azure-Samples/storage-python-getting-started/

To get the source code of the SDK via git, type:
git clone git://github.com/Azure-Samples/storage-python-getting-started.git
cd .\storage-python-getting-started

##Minimum Requirements
Python 2.7, 3.3, or 3.4.
To install Python, please go to https://www.python.org/downloads/

## More information
  - What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/  
  - Getting Started with Blobs - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-blob-storage/
  - Blob Service Concepts - http://msdn.microsoft.com/en-us/library/dd179376.aspx 
  - Blob Service REST API - http://msdn.microsoft.com/en-us/library/dd135733.aspx 
  - Getting Started with Files - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-file-storage/  
  - File Service Concepts - http://msdn.microsoft.com/en-us/library/dn166972.aspx  
  - File Service REST API - http://msdn.microsoft.com/en-us/library/dn167006.aspx  
  - Getting Started with Tables - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-table-storage/
  - Table Service Concepts - http://msdn.microsoft.com/en-us/library/dd179463.aspx
  - Table Service REST API - http://msdn.microsoft.com/en-us/library/dd179423.aspx
  - Getting Started with Queues - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-queue-storage/
  - Queue Service Concepts - http://msdn.microsoft.com/en-us/library/dd179353.aspx
  - Queue Service REST API - http://msdn.microsoft.com/en-us/library/dd179363.aspx
  - Queue Service Python API - http://azure.github.io/azure-storage-python/ref/azure.storage.queue.html
  - Storage Emulator - http://azure.microsoft.com/en-us/documentation/articles/storage-use-emulator/