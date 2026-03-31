# Real-Time Weather Streaming Pipeline (Azure, Databricks, Fabric)

## Overview

This project is a real-time data pipeline built to understand how streaming systems work in practice. It collects live weather data from an external API, streams it through Azure Event Hub, processes it using Databricks, and visualizes the output using Microsoft Fabric and Power BI.

The goal was to build an end-to-end working pipeline and understand how data flows continuously in a real-time setup.

---

## Architecture

Weather API → Azure Function → Event Hub → Databricks → Fabric EventStream → Eventhouse → Power BI

---

## Technologies Used

* Python
* Azure Function
* Azure Event Hub
* Azure Databricks (PySpark)
* Microsoft Fabric (EventStream, Eventhouse)
* Power BI
* Azure Key Vault

---

## Workflow

### 1. Data Ingestion

An Azure Function calls the weather API at regular intervals (every 30 seconds).
The response is converted into JSON format and sent to Azure Event Hub.

---

### 2. Streaming Layer

Event Hub receives the incoming events and acts as a buffer between ingestion and processing.
It enables continuous data flow and decouples upstream and downstream systems.

---

### 3. Processing Layer

Azure Databricks reads data from Event Hub using Structured Streaming.

* Processes data using micro-batches
* Uses checkpointing to maintain state and avoid data loss
* Applies basic transformations before forwarding

---

### 4. Fabric Integration

Event Hub is connected to Microsoft Fabric using EventStream.

* EventStream ingests data from Event Hub
* Routes the data into Eventhouse for storage and querying

---

### 5. Storage and Querying

Eventhouse stores the processed data in tabular format.
Data is queried using KQL.

Example:

```kql
weather-table | count
```

---

## Note on Data

This project uses a live weather API.
No static or sample dataset is stored in this repository.

Example schema of incoming data:

```json
{
  "location": "Chennai",
  "temperature": 32,
  "humidity": 70,
  "timestamp": "2026-03-31T10:00:00Z"
}
```

---

### 6. Visualization

Power BI is connected to Eventhouse to build dashboards.

The dashboard includes:

* Temperature trends
* Region-based analysis
* Basic distribution visuals

---

## Sample Code

### Producer Logic

```python
while True:
    fetch_weather_data()
    send_to_eventhub()
    time.sleep(30)
```

---

### Databricks Streaming

```python
query = streaming_df.writeStream \
    .foreachBatch(process_batch) \
    .option("checkpointLocation", checkpoint_path) \
    .start()

query.awaitTermination()
```

---

## Challenges Faced

* Permission issues with DBFS public path
* Event Hub connection setup required debugging
* Understanding streaming flow took time initially
* Debugging streaming jobs was more complex than batch jobs

---

## Learning Outcomes

* Difference between batch and real-time pipelines
* Working knowledge of Azure streaming services
* Hands-on experience with Spark Structured Streaming
* Importance of checkpointing in streaming systems
* End-to-end pipeline design and integration

---

## Limitations

* Minimal transformations applied
* Not optimized for production scale
* Single partition used in Event Hub
* No monitoring or alerting implemented

---

## Future Improvements

* Integrate Delta Lake for storage
* Increase Event Hub partitions for scalability
* Add monitoring and alerting (Azure Monitor / KQL alerts)
* Improve transformation and enrichment logic
* Implement CI/CD for deployment

---

## Author

Ponmani Boopathy P
B.Tech AI & Data Science
