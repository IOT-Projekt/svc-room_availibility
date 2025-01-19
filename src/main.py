import streamlit as st
import json
import time
from kafka_handler import KafkaConfig, setup_kafka_consumer

# Function to get room status from Kafka
def get_room_status(consumer):
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        return data.get('room_status', False)

# Streamlit app
def main():
    st.title("Room Availability Dashboard")

    # Set up Kafka consumer
    kafka_config = KafkaConfig()
    consumer = setup_kafka_consumer(kafka_config, ["room_status"])

    status_placeholder = st.empty()

    while True:
        room_status = get_room_status(consumer)

        if room_status:
            status_placeholder.success("Room is available", icon="✅")
        else:
            status_placeholder.error("Room is booked", icon="❌")

        time.sleep(5)  # Update every 5 seconds

if __name__ == "__main__":
    main()