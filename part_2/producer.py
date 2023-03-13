import faker
import pika

from models import Contact
import connect

NUMBER_OF_USERS = 10


def main():
    fake = faker.Faker("uk-UA")
    users = []

    for _ in range(NUMBER_OF_USERS):
        user = Contact(fullname=fake.name(), email=fake.email())
        user.save()
        users.append(user)

    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange="task_mock", exchange_type="direct")
    channel.queue_declare(queue="task_queue", durable=True)
    channel.queue_bind(exchange="task_mock", queue="task_queue")

    for user in users:
        channel.basic_publish(
            exchange="task_mock",
            routing_key="task_queue",
            body=str(user.id),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.TRANSIENT_DELIVERY_MODE
                )
        )

    connection.close()


if __name__ == '__main__':
    main()
