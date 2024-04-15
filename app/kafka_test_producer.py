from aiokafka import AIOKafkaProducer
import asyncio

async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='kafka:29092')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("test-topic", b"Super-pooper message")
    finally:
        await producer.stop()


asyncio.run(send_one())
