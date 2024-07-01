import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import os

class Counter:
    def __init__(self):
        # Here we are initializing the CosmosDB connection
        connection_string = os.environ['AzureResumeConnectionString']
        self.client = cosmos_client.CosmosClient.from_connection_string(connection_string)
        self.database = self.client.get_database_client("cloud-resume-francisco")
        self.container = self.database.get_container_client("counter-container")
       
        
    def get_count(self):
        try:
            item = self.container.read_item(item="1", partition_key="1")
            return item['counter']
        except exceptions.CosmosResourceNotFoundError:
            # if the counter does not exist, it gets initialized
            self.container.create_item({
                'id': '1',
                'counter': 0
            })
            return 0
        
    def increment_count(self):
        # Here we are incrementing the counter
        