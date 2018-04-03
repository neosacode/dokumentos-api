# Generated by Django 2.0.3 on 2018-04-03 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('abbr', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countrys',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ref', models.CharField(max_length=300)),
                ('error', models.CharField(max_length=300, null=True)),
                ('file', models.URLField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('valid', 'valid'), ('invalid', 'invalid')], max_length=30, verbose_name='status')),
                ('webhook', models.URLField(blank=True, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Country')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('abbr', models.CharField(max_length=50)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='documents.Country')),
            ],
            options={
                'verbose_name': 'Model',
                'verbose_name_plural': 'Models',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('abbr', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
            },
        ),
        migrations.AddField(
            model_name='model',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='documents.Type'),
        ),
        migrations.AddField(
            model_name='document',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Model'),
        ),
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Type'),
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='model',
            unique_together={('country', 'type', 'abbr')},
        ),
    ]
