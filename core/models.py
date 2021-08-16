import uuid
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    author = models.CharField(max_length=100, blank=False, null=False)
    publication = models.DateTimeField(blank=False, null=False)
    available_quantity = models.IntegerField(blank=False, null=False)
    users = models.ManyToManyField(User, blank=True, related_name="books")

    class Meta:
        db_table = 'books'

