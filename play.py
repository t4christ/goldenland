import os
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient

AZURE_TENANT_ID="d0b6f44a-7691-40f4-ba05-ab5986b39ac8"
AZURE_CLIENT_ID="dc42e200-aac0-47fd-9260-97a0e5c96326"
AZURE_CLIENT_SECRET="fl88Q~IYBNRrtpWG1P2F5J9Bw2Ep7ZIsTaNJ.b_7"

subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID','e44e3b9c-d405-4a5d-b1a3-6490992e0a96') # your Azure Subscription Id
credentials = ClientSecretCredential(
    client_id=os.environ['AZURE_CLIENT_ID'],
    client_secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant_id=os.environ['AZURE_TENANT_ID']
)




resource_client = ResourceManagementClient(credentials, subscription_id)
storage_client = StorageManagementClient(credentials, subscription_id)
storage_accounts = [item for item in storage_client.storage_accounts.list()]

# print(storage_accounts)

# # Retrieve storage account key
# storage_keys = storage_client.storage_accounts.list_keys(resource_client, storage_accounts)
# storage_keys = {v.key_name: v.value for v in storage_keys.keys}
# print('\tKey 1: {}'.format(storage_keys['key1']))
# print('\tKey 2: {}'.format(storage_keys['key2']))

# # Connect to storage account
# _block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key, endpoint_suffix=azure_environment.suffixes.storage_endpoint, protocol='https')

# # Get containers
# containers = _block_blob_service.list_containers()

# # For every container, retrieve acl
# _block_blob_service.get_container_acl(container_name)




# az role assignment create \
#     --role "Storage Account Contributor" \
#     --assignee "dc42e200-aac0-47fd-9260-97a0e5c96326" \
#     --scope "/subscriptions/e44e3b9c-d405-4a5d-b1a3-6490992e0a96/resourceGroups/CommsworthWeb/providers/Microsoft.Storage/storageAccounts/read"



