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
import random, config
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
#  - Table Service Python API - http://azure.github.io/azure-storage-python/ref/azure.storage.table.html
#  - Storage Emulator - http://azure.microsoft.com/en-us/documentation/articles/storage-use-emulator/
#

class table_samples():

    # Runs all samples for Azure Storage Table service.
    # Input Arguments:
    # account - CloudStorageAccount to use for running the samples
    def run_all_samples(account):
        print('Azure Storage Table sample - Starting.')
        table_service = None
        try:
            table_service = account.create_table_service()
            table_name = 'tablebasics' + randomtablename(6)

            # Create a new table
            print('Create a table with name - ' + table_name)

            try:
                table_service.create_table(table_name)
            except Exception as err:
                print('Error creating table, ' + table_name + 'check if it already exists')
 
            # Create a sample entity to insert into the table
            customer = {'PartitionKey': 'Harp', 'RowKey': '1', 'email' : 'harp@contoso.com', 'phone' : '555-555-5555'}

            # Insert the entity into the table
            print('Inserting a new entity into table - ' + table_name)
            table_service.insert_entity(table_name, customer)
            print('Successfully inserted the new entity')

            # Demonstrate how to query the entity
            print('Read the inserted entity.')
            entity = table_service.get_entity(table_name, 'Harp', '1')
            print(entity['email'])
            print(entity['phone'])


            # Demonstrate how to update the entity by changing the phone number
            print('Update an existing entity by changing the phone number')
            customer = {'PartitionKey': 'Harp', 'RowKey': '1', 'email' : 'harp@contoso.com', 'phone' : '425-123-1234'}
            table_service.update_entity(table_name, customer)


            # Demonstrate how to query the updated entity, filter the results with a filter query and select only the value in the phone column
            print('Read the updated entity with a filter query')
            entities = table_service.query_entities(table_name, filter="PartitionKey eq 'Harp'", select='phone')
            for entity in entities:
                print(entity['phone'])


            # Demonstrate how to delete an entity
            print('Delete the entity')
            table_service.delete_entity(table_name, 'Harp', '1')
            print('Successfully deleted the entity')

            # Demonstrate deleting the table, if you don't want to have the table deleted comment the below block of code
            print('Deleting the table.')
            table_service.delete_table(table_name)
            print('Successfully deleted the table')

            print('Azure Storage Table sample - Completed.')
        except Exception as e:
            if (config.IS_EMULATED):
                print('Error occurred in the sample. If you are using the emulator, please make sure the emulator is running.', e)
            else: 
                print('Error occurred in the sample. Please make sure the account name and key are correct.', e)

    # Gets 6 random characters to append to Table name.
    def randomtablename(length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))