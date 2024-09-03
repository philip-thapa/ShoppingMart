# Generated by Django 4.2 on 2024-09-03 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0002_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(db_column='addressType', default='Home', max_length=8),
        ),
        migrations.AlterField(
            model_name='address',
            name='user_id',
            field=models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
    ]
