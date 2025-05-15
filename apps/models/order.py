from django.db.models import Model, CharField, DecimalField, TextField, ForeignKey, \
    DateTimeField, CASCADE, TextChoices


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', on_delete=CASCADE, related_name='districts')


class OrderAddress(Model):
    address = CharField(max_length=255)
    district = CharField(max_length=255)


class Order(Model):
    class StatusType(TextChoices):
        PENDING = 'pending', 'Pending'
        SHIPPED = 'shipped', 'Shipped'
        IN_TRANSIT = 'in_transit', 'In Transit'
        DELIVERED = 'delivered', 'Delivered'
        FAILED = 'failed', 'Failed'

    name = CharField(max_length=255)
    phone_number = CharField(max_length=255)
    status = CharField(max_length=255, choices=StatusType, default=StatusType.PENDING)
    created_at = DateTimeField(auto_now_add=True)
    stream_ordering = CharField(max_length=255)
    payment = ForeignKey('apps.Payment', on_delete=CASCADE, related_name='orders')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='orders')
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='orders')
    region = ForeignKey('apps.Region', on_delete=CASCADE, related_name='orders')
    order_address = ForeignKey('apps.OrderAddress', on_delete=CASCADE, related_name='orders')


class Delivery(Model):
    class Meta:
        verbose_name_plural = "deliveries"

    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField(null=True, blank=True)
    delivery_time = DateTimeField()
    phone_number = CharField(max_length=255)
