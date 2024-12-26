import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from stock_market_app.models import Agency, Broker, Producer, Product, Batch, BatchProduct, Client, ClientPurchase, \
    Transaction


class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **kwargs):
        agencies = [Agency.objects.create(name=f"Agency {i}", address=f"Address {i}") for i in range(1, 6)]

        brokers = [Broker.objects.create(
            name=f"Broker {i}",
            fixed_monthly_fee=random.randint(1000, 5000),
            agency=random.choice(agencies)
        ) for i in range(1, 11)]

        producers = [Producer.objects.create(
            name=f"Producer {i}",
            address=f"Producer Address {i}",
            phone=f"+123456789{i}",
            email=f"producer{i}@example.com"
        ) for i in range(1, 11)]

        # Создаем продукты
        products = [Product.objects.create(
            name=f"Product {i}",
            production_date=datetime.now().date() - timedelta(days=random.randint(30, 365)),
            expiration_date=datetime.now().date() - timedelta(days=random.randint(1, 30)),
            unit="pcs",
            producer=random.choice(producers)
        ) for i in range(1, 21)]

        batches = []
        for broker in brokers:
            for _ in range(random.randint(1, 3)):
                batch = Batch.objects.create(
                    supply_conditions=random.choice(['prepayment', 'no_prepayment']),
                    contract_date=datetime.now().date() - timedelta(days=random.randint(30, 180)),
                    shipment_date=datetime.now().date() - timedelta(days=random.randint(1, 30)),
                    broker=broker
                )
                batches.append(batch)

        batch_products = [BatchProduct.objects.create(
            batch=random.choice(batches),
            product=random.choice(products),
            quantity=random.randint(10, 100),
            price_per_unit=random.uniform(10.0, 100.0)
        ) for i in range(1, 31)]

        clients = [Client.objects.create(
            name=f"Client {i}",
            address=f"Client Address {i}",
            phone=f"+987654321{i}",
            email=f"client{i}@example.com",
            registration_date=datetime.now().date() - timedelta(days=random.randint(30, 365))
        ) for i in range(1, 11)]

        for client in clients:
            broker = random.choice(brokers)
            print(f"Assigning purchases for {client.name} with broker {broker.name}")

            broker_batches = [batch for batch in batches if batch.broker == broker]

            for _ in range(random.randint(1, 5)):  # Каждый клиент может сделать от 1 до 5 покупок
                batch = random.choice(broker_batches)
                ClientPurchase.objects.create(
                    client=client,
                    batch=batch,
                    quantity=random.randint(1, 10),
                    purchase_date=datetime.now().date() - timedelta(days=random.randint(1, 90)),
                    total_price=random.uniform(50.0, 500.0)
                )

        transactions = [Transaction.objects.create(
            batch=random.choice(batches),
            total_amount=random.uniform(100.0, 1000.0),
            transaction_date=datetime.now().date() - timedelta(days=random.randint(1, 90))
        ) for i in range(1, 11)]

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with test data!'))
