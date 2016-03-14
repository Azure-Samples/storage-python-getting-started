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

from azure.storage import CloudStorageAccount
from azure.storage.queue import QueueService
from azure.storage.queue import Queue
from azure.storage.queue import QueueMessage
import config


# -------------------------------------------------------------
# <summary>
# Azure Queue Service Sample - The Queue Service provides reliable messaging for workflow processing and for communication 
# between loosely coupled components of cloud services. This sample demonstrates how to perform common tasks including 
# inserting, peeking, getting and deleting queue messages, as well as creating and deleting queues. 
# 
# Note: This sample uses the .NET 4.5 asynchronous programming model to demonstrate how to call the Storage Service using the 
# storage client libraries asynchronous API's. When used in real applications this approach enables you to improve the 
# responsiveness of your application. Calls to the storage service are prefixed by the await keyword. 
# 
# Documentation References: 
# - What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/
# - Getting Started with Queues - http://azure.microsoft.com/en-us/documentation/articles/storage-dotnet-how-to-use-queues/
# - Queue Service Concepts - http://msdn.microsoft.com/en-us/library/dd179353.aspx
# - Queue Service REST API - http://msdn.microsoft.com/en-us/library/dd179363.aspx
# - Queue Service Python API - http://azure.github.io/azure-storage-python/
# - Storage Emulator - http://msdn.microsoft.com/en-us/library/azure/hh403989.aspx
# </summary>
# -------------------------------------------------------------

class QueueSamples():

    def RunSamples(account):
        try:
            #declare variables
            queuename = "pythonqueue6"

            #create a new queue service that can be passed to all methods
            queue_service = CloudStorageAccount.create_queue_service(account)

            #Basic queue operations such as creating a queue and listing all queues in your account
            QueueSamples.basic_queue_operations(queue_service, queuename)

            #Add a message to a queue in your account
            QueueSamples.basic_queue_message_operations(queue_service, queuename)

            #List all queues in your account
            #QueueSamples.delete_queue(queue_service, queuename)
        except Exception as e:
            print('Error occurred in the sample. If you are using the emulator, please make sure the emulator is running.', e)


    def basic_queue_operations(queue_service, queuename):
        # Create a queue or leverage one if already exists
        print('Attempting create of queue: ', queuename)
        queue_service.create_queue(queuename, fail_on_exist=False)
        print('Successfully created queue: ', queuename)

        #List all queues in the account
        print('Listing all queues in the account')
        queues = list(queue_service.list_queues())
        for queue in queues:
            print(queue.name)

    def basic_queue_message_operations(queue_service, queuename):
        # Add 5 messages to the queue.
        # the message will be visible in 10 seconds and will expire in 1000 seconds. 
        # if you do not specify time_to_live, the message will expire after 7 days
        # if you do not specify visibility_timeout, the message will be immediately visible
        messagename = "test message"
        for i in range(1, 5):
            queue_service.put_message(queuename, messagename + str(i), time_to_live=1000, visibility_timeout=10)
            print ('Successfully added message: ', messagename + str(i))
            i=i+1

        # Get length of queue
        # Retrieve queue metadata which contains the approximate message count ie.. length. 
        # Note that this may not be accurate given dequeueing operations that could be happening in parallel 
        metadata = queue_service.get_queue_metadata(queuename)
        length = metadata.approximate_message_count
        print('Length of the queue: ', length)

        #Look at the first message only without dequeueing it
        messages = queue_service.peek_messages(queuename)
        for message in messages:
            print('Peeked message content is: ', message.content)

        #Look at the first 5 messages only without any timeout without dequeueing it
        messages = queue_service.peek_messages(queuename,num_messages=5)
        for message in messages:
            print('Peeked message content is: ', message.content)

        #Look at the first 10 messages but with a 5 sec timeout without dequeueing it
        messages = queue_service.peek_messages(queuename, num_messages=10, timeout=5)
        for message in messages:
            print('Peeked message content is: ', message.content)

        #Dequeuing messages
        #First get the message, to read and process it.
        messages = queue_service.get_messages(queuename, num_messages=1, visibility_timeout=60)
        for message in messages:
            print('Message for dequeueing is: ', message.content)

        # Then delete it. 
        #Deleting requires the message id and pop receipt (returned by get_messages)
        # Attempt for 60 seconds. Timeout if it does not complete by that time.
        queue_service.delete_message(queuename, messages[0].id, messages[0].pop_receipt, timeout=60)      
        print('Successfully dequeued message')


    #Delete the queue
    def delete_queue(queue_service, queuename):
        #Delete the queue. 
        #Warning: This will delete all the messages that are contained in it.
        print('Attempting delete of queue: ', queuename)
        queue_service.delete_queue(queuename)    
        print('Successfully deleted queue: ', queuename)
