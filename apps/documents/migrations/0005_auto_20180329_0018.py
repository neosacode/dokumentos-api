# Generated by Django 2.0.3 on 2018-03-29 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20180323_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='webhook',
            field=models.URLField(blank=True, null=True),
        ),
    ]
