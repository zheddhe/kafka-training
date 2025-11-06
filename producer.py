from kafka import KafkaProducer


kafka_producer = KafkaProducer(
  bootstrap_servers="localhost:9092"
)

for i in range(1, 30):
    kafka_producer.send(
        topic="test",
        value=f"New message # {i}".encode("utf-8"),
        # la clef vaudra '0' pour les messages pairs, et '1' pour les messages impairs
        # les messages sont ordonnés au sein d'une même partition
        key=f"{i % 2}".encode("utf-8")
    )

kafka_producer.flush()
