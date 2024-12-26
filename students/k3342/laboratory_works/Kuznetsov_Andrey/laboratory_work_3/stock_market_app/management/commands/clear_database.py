from django.core.management.base import BaseCommand
from stock_market_app.models import Transaction, ClientPurchase, BatchProduct, Batch, Product, Producer, Client, Broker, Agency


class Command(BaseCommand):
    help = 'Clear all data from the database'

    def handle(self, *args, **kwargs):
        self.clear_data()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from the database!'))

    def clear_data(self):
        """Clear all data in reverse order of relationships."""
        Transaction.objects.all().delete()
        ClientPurchase.objects.all().delete()
        BatchProduct.objects.all().delete()
        Batch.objects.all().delete()
        Product.objects.all().delete()
        Producer.objects.all().delete()
        Client.objects.all().delete()
        Broker.objects.all().delete()
        Agency.objects.all().delete()
