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

import uuid
import random
import string
import io
import tempfile
import fileinput
import os
import time
import config
import azure.common

from azure.common import AzureException
from azure.storage import CloudStorageAccount
from azure.storage.file import FileService

#
# Azure File Service Sample - Demonstrate how to perform common tasks using the Microsoft Azure File Service.  
#  
# Documentation References:  
#  - What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/  
#  - Getting Started with Files - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-file-storage/  
#  - File Service Concepts - http://msdn.microsoft.com/en-us/library/dn166972.aspx  
#  - File Service REST API - http://msdn.microsoft.com/en-us/library/dn167006.aspx  
#  - Storage Emulator - http://azure.microsoft.com/en-us/documentation/articles/storage-use-emulator/
#  

class file_samples():

    # Runs all samples for Azure Storage File service.
    # Input Arguments:
    # account - CloudStorageAccount to use for running the samples
    @staticmethod
    def run_all_samples(account):

        print('Azure Storage File sample - Starting.')
        
        try:
            #declare variables
            file_service = None
            filename = 'filesample' + file_samples.randomfilename(6)
            
            # Create a new file service that can be passed to all methods
            file_service = account.create_file_service()

            # Create and upload a text file to 'myshare/mydirectory/filename' in your Azure Files account.
            file_samples.file_from_text_sample(file_service, filename)

            # Upload a local file to 'myshare2/filename' to your Azure Files account.
            file_samples.file_from_path_sample(file_service, filename)

            # Download file from 'myshare/mydirectory/filename' in your Azure Files to your local temp folder.
            file_samples.file_download_sample(file_service, filename)

            # List all files in your myshare folder
            file_samples.list_files_or_dirs(file_service)

        except Exception as e:
            if (config.IS_EMULATED):
                print('Emulator currently does not support Azure Files.', e)
            else: 
                print('Error occurred in the sample. Please make sure the account name and key are correct.', e) 

        finally:
            # Demonstrate deleting the file, if you don't want to have the file deleted comment the below block of code
            if file_service is not None:
                file_samples.file_delete_samples(file_service, filename)

            print('Azure Storage File sample - Completed.')
    

    # Demonstrate how to create share location, file directory, and upload a text file to Azure Files.
    # An account can contain an unlimited number of shares that can store unlimited number of files.
    def file_from_text_sample(file_service, filename):
        print('Attempting to create a sample file from text for upload demonstration.')    

        try:
            # Creating an SMB file share in your Azure Files account.
            # All directories and share must be created in a parent share.
            # Max capacity: 5TB per share
            print('Creating sample share.') 
            file_service.create_share('myshare')
            print('Sample share "myshare" created.')

            # Creating an optional file directory in your Azure Files account.
            print('Creating a sample directory.')    
            file_service.create_directory(
                'myshare', 
                'mydirectory')
            print('Sample directory "myshare/mydirectory" created.')

            # Uploading text to myshare/mydirectory/my_text_file.txt in Azure Files account.
            # Max capacity: 1TB per file
            print('Uploading a sample file from text.')   
            file_service.create_file_from_text(
                'myshare',              # share        
                'mydirectory',          # directory path - root path if none
                filename,     # destination file name
                'Hello World! - from text sample')    # file text
            print('Sample file "' + filename + '" created and uploaded to: myshare/mydirectory')
            print('Completed successfully - file from text uploaded.') 

        except Exception as e:
            print('********Error***********')
            print(e)
    
    # Demonstrate how to create a share and upload a file from a local temporary file path
    def file_from_path_sample(file_service, filename):
        
        print('Attempting to upload a sample file from path for upload demonstration.')  

        try:
            # Declare variables
            my_share2 = 'myshare2' 

            # Creating a temporary file to upload to Azure Files
            print('Creating a temporary file from text.') 
            with tempfile.NamedTemporaryFile(delete=False) as my_temp_file: #
                my_temp_file.file.write(b"Hello world!")
            print('Sample temporary file created.') 

            # Creating an SMB file share
            # All directories and share must be created in a parent share
            # Max capacity: 5TB per share
            print('Creating a sample share for demonstration.') 
            file_service.create_share(my_share2)
            print('Sample share "myshare2" created.')

            # Uploading my_temp_file to myshare/mydirectory folder in Azure Files
            # Max capacity: 1TB per file
            print('Uploading a sample file from local path.')                    
            file_service.create_file_from_path(
                my_share2,              # share name
                None,                   # directory path - root path if none
                filename,               # destination file name
                my_temp_file.name)      # full source path with file name

            print('Sample file "' + filename + '" uploaded from path to "myshare2".')

            # Close the temp file
            my_temp_file.close()

            print('Completed successfully - file from path uploaded to: myshare2/' + filename) 

        except Exception as e:
            print('********Error***********')
            print(e)

    # Demonstrate how to download a file from Azure Files
    # The following example download the file that was previously uploaded to Azure Files
    def file_download_sample(file_service, filename):
        print('Attempting to download a sample file from Azure files for demonstration.')

        try:
            destination_file = tempfile.tempdir + '\mypathfile.txt'

            file_service.get_file_to_path(
                'myshare',              # share name
                'mydirectory',          # directory path
                filename,               # source file name
                destination_file)       # destinatation path with name

            print('Completed successfully - Azure Files downloaded file to: ' + destination_file)

        except Exception as e:
            print('********Error***********')
            print(e)

    # Demonstrate how to list files and directories contains under Azure File share
    def list_files_or_dirs(file_service):
        print('Attempting to list all files and directories in share folder:')

        try:
            # Create a generator to list directories and files under share 'myshare'
            generator = file_service.list_directories_and_files('myshare')
            # Prints all the directories and files under the share
            for file_or_dir in generator:
                print(file_or_dir.name)
        
            print('Completed successfully - listed files and directories under share "myshare".')
        
        except Exception as e:
            print('********Error***********')
            print(e)

    # Demonstrate how to delete azure files created for this demonstration
    # Warning: Deleting a share or direcotry will also delete all files and directories that are contained in it.
    def file_delete_samples(file_service, filename):
        print('Deleting all samples created for demonstration.')

        try:
            # Deleting file: 'myshare/mydirectory/filename'
            print('Deleting a sample file.')
            file_service.delete_file(
                'myshare',              # share name
                'mydirectory',          # directory path
                filename)               # file name to delete
            print('Sample file "myshare/mydirectory/' + filename + '" deleted.')

            # Deleting directory: 'myshare/mydirectory'
            print('Deleting sample directory and all files and directories under it.')
            file_service.delete_directory(
                'myshare',              # share name
                'mydirectory')          # directory path
            print('Sample directory "myshare/mydirectory" deleted.')

            # Deleting share: 'myshare'
            print('Deleting sample share "myshare" and all files and directories under it.')
            file_service.delete_share(
                'myshare')              # share name
            print('Sample share "myshare" deleted.')
            
            # Deleting share: 'myshare'
            # Warning - This will delete all files and directories under this share
            print('Deleting sample share "myshare2" and all files and directories under it.')
            file_service.delete_share(
                'myshare2')              # share name
            print('Sample share "myshare2" deleted.')

            print('Completed successfully - all Azure Files samples deleted.')

        except Exception as e:
            print('********Error***********')
            print(e)

    # Get random characters to append to File name
    def randomfilename(length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))



