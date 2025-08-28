import logging
from azure.storage.blob import BlobServiceClient
import os
import requests
import json
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.eventhub import EventHubProducerClient, EventData

app = func.FunctionApp()

# --- Configuration from environment variables ---
api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
event_hubs_hostname = os.environ.get("EVENT_HUB_NAMESPACE_HOSTNAME")
event_hub_name = os.environ.get("EVENT_HUB_NAME")
stock_symbol = 'MSFT'

# Use Managed Identity to authenticate
credential = DefaultAzureCredential()

@app.schedule(schedule="0 */1 * * * *", arg_name="myTimer", run_on_startup=False) 
def StockPriceProducer(myTimer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function executed.')

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={api_key}"

    try:
        producer_client = EventHubProducerClient(fully_qualified_namespace=event_hubs_hostname, eventhub_name=event_hub_name, credential=credential)

        response = requests.get(url)
        response.raise_for_status() # Raises an exception for bad status codes
        data = response.json()

        quote = data.get('Global Quote', {})
        price_str = quote.get('05. price')

        if not price_str:
            logging.warning(f"Could not retrieve a valid stock quote. API Response: {data}")
            return

        event_body = {
            "Symbol": stock_symbol,
            "Price": float(price_str),
            "Timestamp": quote.get('07. latest trading day') # Or use current time
        }

        with producer_client:
            event_data_batch = producer_client.create_batch()
            event_data_batch.add(EventData(json.dumps(event_body)))
            producer_client.send_batch(event_data_batch)

        logging.info(f"Successfully sent price for {stock_symbol}: {price_str}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def GetDataForDashboard(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for dashboard data.')

    try:
        # Define all necessary variables inside the function
        storage_account_name = os.environ.get("STORAGE_ACCOUNT_NAME")
        container_name = "processed-data"
        storage_account_url = f"https://{storage_account_name}.blob.core.windows.net"

        blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=credential)
        container_client = blob_service_client.get_container_client(container_name)
        
        # ... rest of the function logic remains the same
        blob_list = container_client.list_blobs()
        latest_blob = max(blob_list, key=lambda b: b.last_modified)

        if not latest_blob:
            return func.HttpResponse("No data available yet.", status_code=404)

        blob_client = container_client.get_blob_client(latest_blob.name)
        blob_data = blob_client.download_blob().readall()
        
        lines = blob_data.decode('utf-8').strip().split('\n')
        json_data = [json.loads(line) for line in lines]

        return func.HttpResponse(
            body=json.dumps(json_data),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"An error occurred in GetDataForDashboard: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)