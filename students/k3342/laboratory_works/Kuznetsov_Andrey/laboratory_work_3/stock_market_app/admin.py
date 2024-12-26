from django.contrib import admin
from .models import Agency, Broker, Producer, Product, Batch, BatchProduct, Client, ClientPurchase, Transaction

admin.site.register(Agency)
admin.site.register(Broker)
admin.site.register(Producer)
admin.site.register(Product)
admin.site.register(Batch)
admin.site.register(BatchProduct)
admin.site.register(Client)
admin.site.register(ClientPurchase)
admin.site.register(Transaction)