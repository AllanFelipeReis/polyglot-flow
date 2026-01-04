import asyncio
import json
import pytest
from testcontainers.rabbitmq import RabbitMqContainer
import aio_pika


@pytest.mark.asyncio
async def test_rabbitmq_consumption_integration():
    # Inicia o container do RabbitMQ
    # Usamos a imagem oficial estável
    with RabbitMqContainer("rabbitmq:3.11-management") as rabbit:
        # O Testcontainers no WSL2 as vezes precisa do IP do host ou localhost
        host = rabbit.get_container_host_ip()
        port = rabbit.get_exposed_port(5672)
        connection_url = f"amqp://guest:guest@{host}:{port}/"

        # Aguarda um pouco para o RabbitMQ terminar de subir internamente
        await asyncio.sleep(5)

        # 1. Conectar e enviar mensagem
        connection = await aio_pika.connect_robust(connection_url)
        async with connection:
            channel = await connection.channel()
            queue_name = "order-events-test"
            queue = await channel.declare_queue(queue_name, durable=True)

            payload = {"orderId": 99, "amount": 500, "customerEmail": "it@test.com"}
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(payload).encode()),
                routing_key=queue_name,
            )

            # 2. Tentar consumir (CORREÇÃO AQUI)
            # aio-pika retorna o objeto 'IncomingMessage' ou None
            incoming_message = await queue.get(fail=False)

            async with incoming_message.process():
                data = json.loads(incoming_message.body)
                assert data["orderId"] == 99
                assert data["customerEmail"] == "it@test.com"
