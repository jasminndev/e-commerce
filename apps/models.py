from django.db.models import Model, TextField, ForeignKey, CASCADE, IntegerField, DateField, CharField


class Transaction(Model):
    balance = IntegerField()
    review = TextField(null=True, blank=True)
    created_at = DateField(auto_now_add=True)
    status = CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])
    payment = ForeignKey('apps.Payment', CASCADE, related_name='transactions')








