import argparse
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

kafka_admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092"
)


def delete_topic(topic: str) -> None:
    try:
        kafka_admin_client.delete_topics([topic])
        print(f"Topic '{topic}' deleted (suppression demandée au cluster).")
    except UnknownTopicOrPartitionError:
        print(f"Topic '{topic}' n'existe pas déjà, rien à supprimer.")


def create_topic(topic: str, num_partitions: int, replication_factor: int) -> None:
    topic_list = [
        NewTopic(
            name=topic,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
    ]
    try:
        kafka_admin_client.create_topics(topic_list)
        print(f"Topic '{topic}' created.")
    except TopicAlreadyExistsError:
        print(
            f"Impossible de créer le topic '{topic}': il existe déjà "
            "(ou est encore en cours de suppression côté Kafka)."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Admin Kafka Topics.")
    parser.add_argument("action", choices=["create", "delete"], type=str, nargs=1)
    parser.add_argument("-n", "--name", type=str, required=True, help="Name of the topic")
    parser.add_argument(
        "-p", "--partition", type=int,
        help="Number of partitions (only used in create mode)", default=1
    )
    parser.add_argument(
        "-r", "--replication", type=int,
        help="Replication factor (only used in create mode)", default=1
    )

    args = parser.parse_args()

    action = args.action[0]

    if action == "delete":
        delete_topic(args.name)
    elif action == "create":
        create_topic(args.name, args.partition, args.replication)
