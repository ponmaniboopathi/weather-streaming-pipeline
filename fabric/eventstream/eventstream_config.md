## EventStream Setup (Microsoft Fabric)

1. Open Microsoft Fabric workspace  
2. Go to **Create → Eventstream**  
3. Name: weather-eventstream  

### Add Source
- Source type: Azure Event Hub  
- Select existing namespace  
- Select event hub: weatherstreaming-eventhub  
- Authentication: Connection string  

### Add Destination
- Destination: Eventhouse  
- Database: weather-eventhouse  
- Table: weather-table  

### Data Format
- Format: JSON  
- Mapping: Auto-detect  

### Activation
- Click **Publish**  
- Turn status to **Active**

---