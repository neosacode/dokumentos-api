# Generated by Django 2.0.3 on 2018-03-23 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20180315_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='webhook',
            field=models.URLField(blank=True),
        ),
    ]
