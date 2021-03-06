# Generated by Django 3.2.5 on 2021-07-29 00:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('publication', models.DateTimeField()),
                ('available_quantity', models.IntegerField()),
            ],
            options={
                'db_table': 'books',
            },
        ),
    ]
