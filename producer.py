from kafka import KafkaProducer


def encode_str(string):
    return (string.encode("utf-8"))


kafka_producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    client_id='production_facile',
    value_serializer=encode_str,
    key_serializer=encode_str
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
