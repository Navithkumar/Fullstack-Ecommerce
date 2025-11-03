from django.db import models
import uuid
from django.utils import timezone

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order({self.id}, {self.status})"


class Outbox(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
