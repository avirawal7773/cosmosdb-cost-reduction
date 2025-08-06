import json
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

def get_billing_record(record_id):
    try:
        client = CosmosClient(COSMOS_URI, COSMOS_KEY)
        container = client.get_database_client("billing").get_container_client("records")
        return container.read_item(record_id, partition_key=record_id)
    except:
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        blob_client = blob_service_client.get_container_client("archived-billing").get_blob_client(f"{record_id}.json")
        data = blob_client.download_blob().readall()
        return json.loads(data)
