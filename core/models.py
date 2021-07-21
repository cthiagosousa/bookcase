from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    author = models.CharField(max_length=100, blank=False, null=False)
    publication = models.DateTimeField(blank=False, null=False)

    class Meta:
        db_table = 'books'

