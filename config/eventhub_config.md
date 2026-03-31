
---

``` id="9p2v0a"


## Azure Event Hub Setup

1. Create Namespace
- Go to Azure Portal → Event Hubs → Create
- Name: weatherstreaming-namespace
- Pricing: Basic

2. Create Event Hub
- Name: weather-streaming-eventhub
- Partition count: 1
- Retention: 1 day

3. Create Access Policy
- Go to Shared Access Policies
- Name: RootManageSharedAccessKey
- Copy:
  - Connection String

4. Python Producer Setup

```python
from azure.eventhub import EventHubProducerClient, EventData

connection_str = "<connection_string>"
eventhub_name = "weather-streaming-eventhub"

producer = EventHubProducerClient.from_connection_string(
    conn_str=connection_str,
    eventhub_name=eventhub_name
)

event_data_batch = producer.create_batch()
event_data_batch.add(EventData("test message"))

producer.send_batch(event_data_batch)
producer.close()