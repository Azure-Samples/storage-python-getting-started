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


import config
from azure.storage import CloudStorageAccount
from azure.storage.table import TableService, Entity

#
# Azure Table Service Sample - Demonstrate how to perform common tasks using the Microsoft Azure Table Service
# including creating a table, CRUD operations and different querying techniques.
#
# Documentation References:
#  - What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/
#  - Getting Started with Tables - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-table-storage/
#  - Table Service Concepts - http://msdn.microsoft.com/en-us/library/dd179463.aspx
#  - Table Service REST API - http://msdn.microsoft.com/en-us/library/dd179423.aspx
#  - Storage Emulator - http://azure.microsoft.com/en-us/documentation/articles/storage-use-emulator/
#
# Instructions:
#      This sample can be run using either the Azure Storage Emulator or your Azure Storage
#      account by updating the config.py file with your "AccountName" and "Key".
#
#      To run the sample using the Storage Emulator (default option - Only available on Microsoft Windows OS)
#          1.  Start the Azure Storage Emulator by pressing the Start button or the Windows key and searching for it
#              by typing "Azure Storage Emulator". Select it from the list of applications to start it.
#          2.  Run this script.
#
#      To run the sample using the Storage Service
#          1.  Open the config.py file and set IS_EMULATED to False
#          2.  Create a Storage Account through the Azure Portal and provide your STORAGE_ACCOUNT_NAME and STORAGE_ACCOUNT_KEY in the config.py file.
#              See https://azure.microsoft.com/en-us/documentation/articles/storage-create-storage-account/ for more information.
#          3.  Run this script.
#

class TableSamples():

    # Runs all samples for Azure Storage Table service.
    # Input Arguments:
    # account - CloudStorageAccount to use for running the samples
    @staticmethod
    def run_all_samples(account):

        try:
            print('Azure Storage Table sample - Starting.')
    
            table_service = account.create_table_service(account)

            # Create a new table
            print('Create a table with name - tablebasics301')

            try:
                table_service.create_table('tablebasics301')
            except Exception as err:
                print('Error creating table tablebasics301, check if it already exists')
                quit()

            # Create a sample entity to insert into the table
            customer = {'PartitionKey': 'Harp', 'RowKey': '1', 'email' : 'harp@contoso.com', 'phone' : '555-555-5555'}

            # Insert the entity into the table
            print('Inserting a new entity into table - tablebasics301')
            table_service.insert_entity('tablebasics301', customer)
            print('Successfully inserted the new entity')

            # Demonstrate how to read the entity
            print('Read the inserted entity.')
            entity = table_service.get_entity('tablebasics301', 'Harp', '1')
            print(entity.email)
            print(entity.phone)


            # Demonstrate how to update the entity by changing the phone number
            print('Update an existing entity by changing the phone number')
            customer = {'PartitionKey': 'Harp', 'RowKey': '1', 'email' : 'harp@contoso.com', 'phone' : '425-123-1234'}
            table_service.update_entity('tablebasics301', 'Harp', '1', customer, content_type='application/atom+xml')


            # Demonstrate how to read the updated entity, filter the results with a filter query and select only the value in the phone column
            print('Read the updated entity with a filter query')
            entities = table_service.query_entities('tablebasics301', filter="PartitionKey eq 'Harp'", select='phone')
            for entity in entities:
                print(entity.phone)


            # Demonstrate how to delete an entity
            print('Delete the entity')
            table_service.delete_entity('tablebasics301', 'Harp', '1')
            print('Successfully deleted the entity')

        except Exception as err:
            print('*** Error occured ***')            
            print(err)

        finally:
            # Demonstrate deleting the table, if you don't want to have the table deleted comment the below block of code
            print('Deleting the table.')
            table_service.delete_table('tablebasics301')
            print('Successfully deleted the table')

            print('Azure Storage Table sample - Completed.')
