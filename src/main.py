import streamlit as st
import json
from kafka_handler import KafkaConfig, setup_kafka_consumer
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants
ROOM_AVAILABLE_STR = "Raum B-0.270 ist frei"
ROOM_UNAVAILABLE_STR = "Raum B-0.270 ist belegt"


# Function to get the room status from the message
def get_room_status(message):
    
    logging.info(f"Received message: {message.value}") # TODO: Remove
    payload_str = message.value["message"]
    logging.info(f"Received message: {payload_str}, Type: {type(payload_str)}") # TODO: Remove
    data = json.loads(payload_str)
    logging.info(f"Received message: {data}")
    logging.info(f"Button toggled: {data.get('button_toggled')}")
    return data.get("button_toggled")


def get_kafka_consumer():
    kafka_config = KafkaConfig()
    consumer = setup_kafka_consumer(kafka_config, ["room_status"])
    return consumer

def main():
    # Set up the Kafka consumer
    consumer = get_kafka_consumer()
    
    # Set up the Streamlit app
    st.title("Verfügbare Räume")

    # Create a placeholder for the status message and display the initial status
    status_placeholder = st.empty()
    status_placeholder.success(ROOM_AVAILABLE_STR, icon="✅")

    for message in consumer:
        if get_room_status(message):
            status_placeholder.success(ROOM_AVAILABLE_STR, icon="✅")
        else:
            status_placeholder.error(ROOM_UNAVAILABLE_STR, icon="❌")


if __name__ == "__main__":
    main()
