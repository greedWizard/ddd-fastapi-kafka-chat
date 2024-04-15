from infra.message_brokers.base import BaseMessageBroker
from logic.init import init_container


async def start_kafka():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.producer.start()


async def close_kafka():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.producer.stop()
