from django.db.models import Model, CharField, DecimalField, TextField, ForeignKey, \
    DateTimeField, CASCADE, TextChoices


class Query(Model):
    class StatusType(TextChoices):
        POSITIVE = 'positive', 'Positive',
        NEGATIVE = 'negative', 'Negative',

    description = TextField()
    status = CharField(max_length=255, choices=StatusType, default=StatusType.POSITIVE)
    created_at = DateTimeField(auto_now_add=True)
    stream = ForeignKey('apps.Stream', on_delete=CASCADE, related_name='queries')
    order_address = ForeignKey('apps.OrderAddress', on_delete=CASCADE, related_name='queries')


class Payment(Model):
    card_number = CharField(max_length=255)
    user = ForeignKey('authentication.User', on_delete=CASCADE, related_name='payments')
    amount = DecimalField(max_digits=10, decimal_places=2)
