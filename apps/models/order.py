from django.db.models import Model, CharField, DecimalField, TextField, ForeignKey, \
    DateTimeField, CASCADE, TextChoices, SET_NULL, PositiveIntegerField


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
        NEW = 'new', 'New'
        READY_TO_DELIVER = 'ready to deliver', 'Ready to deliver'
        DELIVERING = 'delivering', 'Delivering'
        DELIVERED = 'delivered', 'Delivered'
        COMPLETED = 'completed', 'Completed'
        MISSED_CALL = 'missed call', 'Missed call'
        ARCHIVED = 'archived', 'Archived'
        CANCELED = 'canceled', 'Canceled'

    first_name = CharField(max_length=255)
    phone_number = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    quantity = PositiveIntegerField(default=1)
    total = DecimalField(max_digits=15, decimal_places=0)
    delivery_time = DateTimeField(null=True, blank=True)
    updated_at = DateTimeField(auto_now=True)
    status = CharField(max_length=255, choices=StatusType, default=StatusType.NEW)
    product = ForeignKey('apps.Product', SET_NULL, related_name='orders', null=True, blank=True)
    owner = ForeignKey('apps.User', SET_NULL, related_name='owner_orders', null=True, blank=True)
    region = ForeignKey('apps.Region', SET_NULL, related_name='orders', null=True, blank=True)
    stream = ForeignKey('apps.Stream', SET_NULL, related_name='orders', null=True, blank=True)
    operator = ForeignKey('apps.User', SET_NULL, related_name='operator_orders', null=True, blank=True)

    @property
    def discount_price(self):
        price = float(self.product.discount_price) - (float(self.stream.discount_price) if self.stream else 0)
        return price


class Delivery(Model):
    class Meta:
        verbose_name_plural = "deliveries"

    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField(null=True, blank=True)
    phone_number = CharField(max_length=255)
