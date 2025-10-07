from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Model, ImageField, CharField, DecimalField, TextField, ForeignKey, \
    DateTimeField, CASCADE, EmailField, TextChoices


class CustomerUser(UserManager):
    def _create_user_object(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = EmailField(max_length=255, unique=True)
    image = ImageField(upload_to='profile_photos', db_default='profile_photos/wllpp.jpg')
    phone_number = CharField(max_length=25, null=True, blank=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomerUser()


class Transaction(Model):
    class StatusType(TextChoices):
        PENDING = 'pending', 'Pending',
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    balance = DecimalField(max_digits=10, decimal_places=2)
    review = TextField()
    status = CharField(max_length=255, choices=StatusType, default=StatusType.PENDING)
    created_at = DateTimeField(auto_now_add=True)
    payment = ForeignKey('apps.Payment', on_delete=CASCADE, related_name='transactions')
