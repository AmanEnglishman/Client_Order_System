from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    """Customer record for the mini CRM."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text='Через запятую')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    def get_tags_list(self):
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class Interaction(models.Model):
    """Client interaction history entry."""
    CONTACT_CALL = 'call'
    CONTACT_EMAIL = 'email'
    CONTACT_MEETING = 'meeting'
    CONTACT_NOTE = 'note'

    CONTACT_TYPE_CHOICES = [
        (CONTACT_CALL, 'Звонок'),
        (CONTACT_EMAIL, 'Email'),
        (CONTACT_MEETING, 'Встреча'),
        (CONTACT_NOTE, 'Заметка'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactions')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='interactions')
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, default=CONTACT_NOTE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client.name} — {self.get_contact_type_display()} ({self.created_at:%Y-%m-%d})"


class Order(models.Model):
    """Order record linked to a client."""
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_DONE, 'Done'),
        (STATUS_CANCELED, 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} — {self.client.name} ({self.status})"
