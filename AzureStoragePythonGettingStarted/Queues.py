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
from azure.storage.queue import Queue, QueueService, QueueMessage
from azure.common import AzureException
import config
import random
import string


# -------------------------------------------------------------
# <summary>
# Azure Queue Service Sample - The Queue Service provides reliable messaging for workflow processing and for communication 
# between loosely coupled components of cloud services. This sample demonstrates how to perform common tasks including 
# inserting, peeking, getting and deleting queue messages, as well as creating and deleting queues. 
# 
# Documentation References: 
# - What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/
# - Getting Started with Queues - https://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-queue-storage/
# - Queue Service Concepts - http://msdn.microsoft.com/en-us/library/dd179353.aspx
# - Queue Service REST API - http://msdn.microsoft.com/en-us/library/dd179363.aspx
# - Queue Service Python API - http://azure.github.io/azure-storage-python/ref/azure.storage.queue.html
# - Storage Emulator - http://msdn.microsoft.com/en-us/library/azure/hh403989.aspx
# </summary>
# -------------------------------------------------------------

class queue_samples():

    def run_all_samples(account):
        try:
            #declare variables
            queuename = "queuesample" + queue_samples.randomqueuename(6)
            
            #create a new queue service that can be passed to all methods
            #queue_service = CloudStorageAccount.create_queue_service(account)
            queue_service = account.create_queue_service()

            #Basic queue operations such as creating a queue and listing all queues in your account
            queue_samples.basic_queue_operations(queue_service, queuename)

            #Add a message to a queue in your account
            queue_samples.basic_queue_message_operations(queue_service, queuename)

            #Delete the queue from your account
            queue_samples.delete_queue(queue_service, queuename)

        except Exception as e:
            if (config.IS_EMULATED):
                print('Error occurred in the sample. Please make sure the Storage emulator is running.', e)
            else: 
                print('Error occurred in the sample. Please make sure the account name and key are correct.', e)

    def basic_queue_operations(queue_service, queuename):
        # Create a queue or leverage one if already exists
        print('Attempting create of queue: ', queuename)
        queue_service.create_queue(queuename)
        print('Successfully created queue: ', queuename)

        #List all queues in the account
        print('Listing all queues in the account')
        queues = queue_service.list_queues()
        for queue in queues:
            print('\t', queue.name)

    def basic_queue_message_operations(queue_service, queuename):
        # Add a number of messages to the queue.
        # if you do not specify time_to_live, the message will expire after 7 days
        # if you do not specify visibility_timeout, the message will be immediately visible
        messagename = "test message"
        for i in range(1, 10):
            queue_service.put_message(queuename, messagename + str(i))
            print ('Successfully added message: ', messagename + str(i))

        # Get length of queue
        # Retrieve queue metadata which contains the approximate message count ie.. length. 
        # Note that this may not be accurate given dequeueing operations that could be happening in parallel 
        metadata = queue_service.get_queue_metadata(queuename)
        length = metadata.approximate_message_count
        print('Approximate length of the queue: ', length)

        #Look at the first message only without dequeueing it
        messages = queue_service.peek_messages(queuename)
        for message in messages:
            print('Peeked message content is: ', message.content)

        #Look at the first 5 messages only without any timeout without dequeueing it
        messages = queue_service.peek_messages(queuename, num_messages=5)
        for message in messages:
            print('Peeked message content is: ', message.content)

        #Dequeuing a message
        #First get the message, to read and process it.
        # Specify num_messages to process a number of messages. If not specified, num_messages defaults to 1
        # Specify visibility_timeout optionally to set how long the message is visible
        messages = queue_service.get_messages(queuename)
        for message in messages:
            print('Message for dequeueing is: ', message.content)
            # Then delete it. 
            #Deleting requires the message id and pop receipt (returned by get_messages)
            # Attempt for 60 seconds. Timeout if it does not complete by that time.
            queue_service.delete_message(queuename, message.id, message.pop_receipt)
            print('Successfully dequeued message')

        #Clear out all messages from the queue
        queue_service.clear_messages(queuename)            
        print('Successfully cleared out all queue messages')

    #Delete the queue
    def delete_queue(queue_service, queuename):
        #Delete the queue. 
        #Warning: This will delete all the messages that are contained in it.
        print('Attempting delete of queue: ', queuename)
        queue_service.delete_queue(queuename)    
        print('Successfully deleted queue: ', queuename)

    # Gets 6 random characters to append to Queue name
    def randomqueuename(length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
