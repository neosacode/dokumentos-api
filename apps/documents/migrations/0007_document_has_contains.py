# Generated by Django 2.0.3 on 2018-04-28 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_document_ocr'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='has_contains',
            field=models.BooleanField(default=False),
        ),
    ]
