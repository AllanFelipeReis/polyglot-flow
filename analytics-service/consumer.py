import pika
import json
import psycopg2
import os
import time

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres-db"),
    "database": os.getenv("DB_NAME", "polyglot_db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASS", "password123"),
}


def update_order_status(order_id, status):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("UPDATE orders SET status = %s WHERE id = %s", (status, order_id))

        conn.commit()
        cur.close()
        conn.close()
        print(f" [DB] Pedido {order_id} atualizado para {status}")
    except Exception as e:
        print(f" [ERR] Erro ao conectar no Postgres: {e}")


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        print(f" [DEBUG] Payload recebido: {data}")

        order_id = data.get("orderId")
        amount = data.get("amount")

        if order_id is None or amount is None:
            print(" [!] Erro: Dados incompletos no JSON. Pulando mensagem.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        print(f" [Analyst] Processando pedido #{order_id} (R$ {amount})")

        # Regra de Negócio
        if float(amount) > 5000:
            print(f" [!] ALTO RISCO detectado no pedido #{order_id}")
            update_order_status(order_id, "FRAUD_DETECTED")
        else:
            print(f" [OK] Pedido #{order_id} aprovado")
            update_order_status(order_id, "PROCESSED")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f" [ERR] Falha ao processar mensagem: {e}")
        # Ack mesmo com erro para não travar a fila, ou use nack se quiser tentar de novo
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
    print(f" [*] Conectando ao RabbitMQ em: {rabbitmq_url}")

    while True:
        try:
            params = pika.URLParameters(rabbitmq_url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            channel.exchange_declare(
                exchange="order-events-exchange", exchange_type="topic", durable=True
            )

            channel.queue_declare(queue="orders-queue", durable=True)

            channel.queue_bind(
                exchange="order-events-exchange", queue="orders-queue", routing_key="#"
            )

            channel.basic_consume(queue="orders-queue", on_message_callback=callback)
            print(" [*] Aguardando mensagens. Para sair pressione CTRL+C")
            channel.start_consuming()
            break
        except Exception as e:
            print(f" [!] Erro: {e}. Tentando novamente em 5s...")
            time.sleep(5)


if __name__ == "__main__":
    main()
