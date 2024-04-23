from typing import List
from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv
import asyncio
import os
from models.models import ID, SessionLocal

load_dotenv()


async def process_ids_async(ids: List[int]):
    from google.cloud import pubsub_v1

    # Publish data to Pub/Sub feed asynchronously
    publisher = pubsub_v1.PublisherClient.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    topic_path = publisher.topic_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("PUBSUB_TOPIC")
    )

    # Query database for each ID and publish data to Pub/Sub feed
    db = SessionLocal()
    try:
        for id in ids:
            # Query database asynchronously
            result = db.query(ID).filter(ID.id == id).first()
            if result:
                data = str(result)
            else:
                # Record doesn't exist, create it and publish
                new_record = ID(id=id)
                db.add(new_record)
                db.commit()
                data = str(new_record)

            # Publish data
            future = publisher.publish(topic_path, data.encode())
            message_id = future.result()
            print(f"Published message ID: {message_id}")

    except Exception as e:
        print(f"Error publishing message: {e}")
        db.rollback()

    finally:
        db.close()


# Function to listen to Pub/Sub feed
async def listen_to_pubsub():
    from google.cloud import pubsub_v1

    subscriber = pubsub_v1.SubscriberClient.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    subscription_path = subscriber.subscription_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("PUBSUB_SUBSCRIPTION")
    )

    def callback(message):
        # Process received message
        data = message.data.decode("utf-8")
        print(f"Received message: {data}")

        # Acknowledge the message
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # Keep the main thread running to continue listening for messages
    await asyncio.Event().wait()


# Run Pub/Sub listener in a separate thread
async def lifespan(app: FastAPI):
    asyncio.create_task(listen_to_pubsub())
    yield


app = FastAPI(lifespan=lifespan)


# Endpoint to submit IDs for processing
@app.post("/process-ids/")
async def process_ids(background_tasks: BackgroundTasks, ids: List[int]):
    # Process IDs asynchronously in the background
    background_tasks.add_task(process_ids_async, ids)
    return {"message": "IDs submitted for processing"}


@app.get("/")
def read_root():
    return {"Hello": "Welcome to FastAPI!"}
