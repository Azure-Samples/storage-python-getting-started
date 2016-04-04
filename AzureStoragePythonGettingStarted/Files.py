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
            filename = 'filesample' + file_samples.randomfilename(6)
            sharename = 'sharesample' + file_samples.randomfilename(6)
            
            # Create a new file service that can be passed to all methods
            file_service = account.create_file_service()

            # Create 
            file_samples.basic_file_operations(file_service, sharename, filename)

            # Delete all Azure Files created in this sample
            file_samples.file_delete_samples(file_service, sharename, filename)

        except Exception as e:
            if (config.IS_EMULATED):
                print('Emulator currently does not support Azure Files.', e)
            else: 
                print('Error occurred in the sample. Please make sure the account name and key are correct.', e) 

        finally:
            print('\n\nAzure Storage File sample - Completed.')
    
    def basic_file_operations(file_service, sharename, filename):
        # Creating an SMB file share in your Azure Files account.
        print('\nAttempting to create a sample file from text for upload demonstration.')   
        # All directories and share must be created in a parent share.
        # Max capacity: 5TB per share
        print('Creating sample share.') 
        file_service.create_share(sharename)
        print('Sample share "'+ sharename +'" created.')

        # Creating an optional file directory in your Azure Files account.
        print('Creating a sample directory.')    
        file_service.create_directory(
            sharename, 
            'mydirectory')
        print('Sample directory "mydirectory" created.')

        # Uploading text to sharename/mydirectory/my_text_file.txt in Azure Files account.
        # Max capacity: 1TB per file
        print('Uploading a sample file from text.')   
        file_service.create_file_from_text(
            sharename,              # share        
            'mydirectory',          # directory path - root path if none
            filename,               # destination file name
            'Hello World! - from text sample')    # file text
        print('Sample file "' + filename + '" created and uploaded to: ' + sharename + '/mydirectory')
  
        # Demonstrate how to create a share and upload a file from a local temporary file path
        print('\nAttempting to upload a sample file from path for upload demonstration.')  
        # Creating a temporary file to upload to Azure Files
        print('Creating a temporary file from text.') 
        with tempfile.NamedTemporaryFile(delete=False) as my_temp_file: #
            my_temp_file.file.write(b"Hello world!")
        print('Sample temporary file created.') 

        # Uploading my_temp_file to sharename/mydirectory folder in Azure Files
        # Max capacity: 1TB per file
        print('Uploading a sample file from local path.')                    
        file_service.create_file_from_path(
            sharename,              # share name
            None,                   # directory path - root path if none
            filename,               # destination file name
            my_temp_file.name)      # full source path with file name

        print('Sample file "' + filename + '" uploaded from path to share: ' + sharename)

        # Close the temp file
        my_temp_file.close()

        # Demonstrate how to download a file from Azure Files
        # The following example download the file that was previously uploaded to Azure Files
        print('\nAttempting to download a sample file from Azure files for demonstration.')

        destination_file = tempfile.tempdir + '\mypathfile.txt'

        file_service.get_file_to_path(
            sharename,              # share name
            'mydirectory',          # directory path
            filename,               # source file name
            destination_file)       # destinatation path with name

        print('Sample file downloaded to: ' + destination_file)


        # Demonstrate how to list files and directories contains under Azure File share
        print('\nAttempting to list all files and directories in share folder:')

        # Create a generator to list directories and files under share
        generator = file_service.list_directories_and_files(sharename)
        # Prints all the directories and files under the share
        for file_or_dir in generator:
            print(file_or_dir.name)
        
        print('Files and directories under share "' + sharename + '" listed.')
        print('\nCompleted successfully - Azure basic Files operations.')

    # Demonstrate how to delete azure files created for this demonstration
    # Warning: Deleting a share or direcotry will also delete all files and directories that are contained in it.
    def file_delete_samples(file_service, sharename, filename):
        print('\nDeleting all samples created for this demonstration.')

        try:
            # Deleting file: 'sharename/mydirectory/filename'
            print('Deleting a sample file.')
            file_service.delete_file(
                sharename,              # share name
                'mydirectory',          # directory path
                filename)               # file name to delete
            print('Sample file "' + filename + '" deleted from: ' + sharename + '/mydirectory' )

            # Deleting directory: 'sharename/mydirectory'
            print('Deleting sample directory and all files and directories under it.')
            file_service.delete_directory(
                sharename,              # share name
                'mydirectory')          # directory path
            print('Sample directory "/mydirectory" deleted from: ' + sharename)

            # Deleting share: 'sharename'
            print('Deleting sample share ' + sharename + ' and all files and directories under it.')
            file_service.delete_share(
                sharename)              # share name
            print('Sample share "' + sharename + '" deleted.')
            print('\nCompleted successfully - Azure Files samples deleted.')

        except Exception as e:
            print('********ErrorDelete***********')
            print(e)

    # Get random characters to append to File name
    def randomfilename(length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))



