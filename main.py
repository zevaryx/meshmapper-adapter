from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging

from fastapi import FastAPI, Path
from aiohttp import ClientSession

from db import connect, Event
from models import WebhookRequest
from settings import Settings

logging.basicConfig(format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s")

settings = Settings.load_settings("config.yaml")

client: ClientSession
db_initialized = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db_initialized
    logging.debug("Starting app")
    client = ClientSession()
    try:
        db_initialized = await connect(settings)
    except Exception as e:
        logging.warning(f"Failed to initialize MongoDB backend: {e}")
    yield
    await client.close()
    logging.debug("Closing app")

app = FastAPI(lifespan=lifespan)

event_lookup = {
    "duplicate_repeater": {
        "name": "Duplicate Repeater",
        "color": "15549029", # Error Red
    },
    "pending_repeater": {
        "name": "Pending Repeater", 
        "color": "16705372", # Warning Yellow
    },
    "offline_observer": {
        "name": "Offline Observer",
        "color": "15549029", # Error Red
    },
    "visitor_message": {
        "name": "Visitor Message",
        "color": "5793266", # Info Blurple
    },
    "test": {
        "name": "Test Message (please ignore)",
        "color": "5793266", # Info Blurple
    }
}

@app.post("/")
async def receive(request: WebhookRequest):
    global db_initialized
    try:
        logging.debug(f"Received request of type {request.event}")
        headers = {"Content-Type": "application/json"}
        event_meta = event_lookup.get(request.event, {"name": request.event.replace("_", " ").capitalize(), "color": "15549029 "})
        
        payload = {
            "username": "",
            "embeds": [{
                "title": f"New Event in {request.region}: {event_meta['name']}",
                "url": f"https://{request.region.lower()}.meshmapper.net/",
                "description": request.message,
                "color": event_meta["color"],
                "timestamp": datetime.fromtimestamp(request.timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                "fields": []
            }]
        }
        
        if request.event not in ["visitor_message", "duplicate_repeater"]:
            for key, value in request.data.items():
                key = key.replace("_", " ").capitalize()
                if isinstance(value, list):
                    value = "\n".join(value)
                elif not isinstance(value, str):
                    value = str(value)
                    
                payload["embeds"][0]["fields"].append({"name": key, "value": value})
            
        for webhook in settings.webhooks:
            if not webhook.regions or request.region in webhook.regions or len(webhook.regions) == 0:
                payload["username"] = webhook.name
                resp = await client.post(str(webhook.url), json=payload, headers=headers)
                resp.raise_for_status()
                
        if db_initialized:
            try:
                await Event(**request.model_dump()).insert()
            except Exception as e:
                logging.warning(f"Failed to save DB model, setting db_initialized to False: {e}")
                db_initialized = False
    except Exception as e:
        logging.critical(f"Failed to process webhook event! {e}", exc_info=True)