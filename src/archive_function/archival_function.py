import json
from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

def archive_old_billing_records():
    client = CosmosClient(COSMOS_URI, COSMOS_KEY)
    container = client.get_database_client("billing").get_container_client("records")

    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client("archived-billing")

    thirty_days_ago = datetime.utcnow() - timedelta(days=90)

    for item in container.query_items(
        query="SELECT * FROM c WHERE c.timestamp < @date",
        parameters=[{"name": "@date", "value": thirty_days_ago.isoformat()}],
        enable_cross_partition_query=True,
    ):
        record_id = item["id"]
        container_client.upload_blob(f"{record_id}.json", json.dumps(item))
        container.delete_item(item=record_id, partition_key=item["partitionKey"])
