import asyncio
import aio_pika
import json
import os


async def process_order(body):
    order_id = body.get("id") or body.get("orderId")
    amount = body.get("totalAmount") or body.get(
        "amount"
    )  # O Java enviou 'totalAmount'
    email = body.get("customerEmail")

    print(f"\n[Analyst] Analisando pedido #{order_id} de {email}")

    # Simulação de regra de negócio
    if amount > 5000:
        print(
            f" [!] ALERTA: Pedido #{order_id} marcado como ALTO RISCO (Valor: {amount})"
        )
    else:
        print(f" [✓] Pedido #{order_id} aprovado na análise de risco.")


async def main():
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

    connection = None
    while connection is None:
        try:
            # O parâmetro timeout ajuda a evitar o erro 111 imediato
            connection = await aio_pika.connect_robust(rabbitmq_url, timeout=20)
            print(" [V] Conectado ao RabbitMQ!")
        except Exception as e:
            print(f" [!] Erro: {e}. Re-tentando em 5s...")
            await asyncio.sleep(5)

    async with connection:
        channel = await connection.channel()

        # 1. Declara a Exchange exatamente como o Spring Cloud Stream faz
        exchange = await channel.declare_exchange(
            "order-events-exchange", aio_pika.ExchangeType.TOPIC, durable=True
        )

        # 2. Declara a fila do Python
        queue = await channel.declare_queue("analytics-service-queue", durable=True)

        # 3. Faz o Bind (Vínculo) para receber as mensagens
        await queue.bind(exchange, routing_key="#")

        print(" [*] Intelligence Service ON. Aguardando mensagens...")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = json.loads(message.body)
                    await process_order(body)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Serviço parado pelo usuário.")
