from kafka import KafkaProducer


def encode_str(string):
    return (string.encode("utf-8"))


kafka_producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    client_id='production_facile',
    value_serializer=encode_str,
    key_serializer=encode_str,
    # --- Retry policy & fiabilité ---
    retries=5,                           # nb de retries
    retry_backoff_ms=100,                # backoff entre 2 retries
    enable_idempotence=True,             # exactement-once côté producer
    acks="all",                          # nécessaire pour l'idempotence
    max_in_flight_requests_per_connection=1,  # préserver l’ordre avec retries
)

for i in range(1, 30):
    kafka_producer.send(
        topic="test",
        value=f"Pas besoin d'encodage # {i}",
        # la clef vaudra '0' pour les messages pairs, et '1' pour les messages impairs
        # les messages sont ordonnés au sein d'une même partition
        key=f"{i % 2}",
    )

kafka_producer.flush()
