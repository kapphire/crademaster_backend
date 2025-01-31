# Generated by Django 5.1.4 on 2025-01-10 18:16

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Execute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('duration', models.IntegerField(default=0)),
                ('agent_os', models.CharField(blank=True, max_length=10, null=True)),
                ('http_user_agent', models.CharField(blank=True, max_length=40, null=True)),
                ('http_referer', models.CharField(blank=True, max_length=40, null=True)),
                ('http_x_forwarded_for', models.CharField(blank=True, max_length=100, null=True)),
                ('profit_percent', models.DecimalField(decimal_places=2, default=0.2, max_digits=10)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
