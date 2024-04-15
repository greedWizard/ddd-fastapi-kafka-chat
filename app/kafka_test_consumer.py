from aiokafka import AIOKafkaConsumer
import asyncio


async def consume():
    consumer = AIOKafkaConsumer(
        'test-topic',
        bootstrap_servers='kafka:29092',
        group_id="chat",
    )

    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


asyncio.run(consume())