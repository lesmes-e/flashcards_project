# Generated by Django 5.1.4 on 2024-12-12 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='user',
        ),
    ]