from django.db.models import Model, ImageField, CharField, DecimalField, TextField, ForeignKey, \
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
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='payments')
    amount = DecimalField(max_digits=10, decimal_places=2)


class Charity(Model):
    description = TextField()
    seller = ForeignKey('apps.Seller', on_delete=CASCADE, related_name='charities')
    amount = DecimalField(max_digits=10, decimal_places=2)


class Post(Model):
    name = CharField(max_length=255)
    description = TextField()
    image = ImageField(upload_to='posts', null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)


class Settings(Model):
    phone_number = CharField(max_length=255)
    telegram_link = CharField(max_length=255)


class Penalty(Model):
    name = CharField(max_length=255)
    amount = DecimalField(max_digits=10, decimal_places=2)
    description = TextField()
    response = TextField()
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='penalties')
