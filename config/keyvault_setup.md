## Azure Key Vault Setup

1. Create Key Vault
- Go to Azure Portal → Key Vault → Create
- Name: pmbkv-weather-streaming
- Region: Same as other resources

2. Add Secret
- Go to Secrets → Generate/Import
- Name: weatherapikey
- Value: <your_api_key>

3. Grant Access
- Go to Access Control (IAM)
- Add Role: Key Vault Secrets User
- Assign to:
  - Azure Function
  - Databricks Managed Identity

4. Access from Python

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

vault_url = "https://pmbkv-weather-streaming.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=vault_url, credential=credential)

secret = client.get_secret("weatherapikey")
print(secret.value)