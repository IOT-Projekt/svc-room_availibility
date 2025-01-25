import streamlit as st
import json
from kafka_handler import KafkaConfig, setup_kafka_consumer
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# String constants for the room status
ROOM_AVAILABLE_STR = "Raum B-0.270 ist frei"
ROOM_UNAVAILABLE_STR = "Raum B-0.270 ist belegt"

# Kafka room status topic from environment variable
KAFKA_ROOM_STATUS_TOPIC = os.getenv("KAFKA_ROOM_STATUS_TOPIC", "room_status")


def get_room_status(message) -> bool:
    """Get the new room status from the received message. Return the new status as a boolean"""
    logging.info(f"Received message: {message.topic} -> {message.value}")

    # Get the button value from the message and rerturn the new status
    data = json.loads(message.value["message"])
    return data.get("button_toggled")


def get_kafka_consumer():
    """Get a Kafkaconfig instance and subscribe a consumer to the topics of the constant"""
    kafka_config = KafkaConfig()
    consumer = setup_kafka_consumer(kafka_config, [KAFKA_ROOM_STATUS_TOPIC])
    return consumer


def main():
    # Set up the Kafka consumer
    consumer = get_kafka_consumer()

    # Set up the Streamlit app for the room status display
    st.title("Verfügbare Räume")

    # Create a placeholder for the status message and display the initial status
    status_placeholder = st.empty()
    status_placeholder.success(ROOM_AVAILABLE_STR, icon="✅")

    # If the consumer gets a new message, update the status message, depending on the room status
    for message in consumer:
        if get_room_status(message):
            status_placeholder.success(ROOM_AVAILABLE_STR, icon="✅")
        else:
            status_placeholder.error(ROOM_UNAVAILABLE_STR, icon="❌")


if __name__ == "__main__":
    main()
