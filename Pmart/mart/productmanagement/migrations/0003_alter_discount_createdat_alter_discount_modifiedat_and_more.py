# Generated by Django 4.2 on 2024-09-19 05:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('productmanagement', '0002_remove_product_file_path_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='createdAt',
            field=models.DateTimeField(db_column='CreatedAt', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='discount',
            name='modifiedAt',
            field=models.DateTimeField(db_column='ModifiedAt', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='product',
            name='createdAt',
            field=models.DateTimeField(db_column='CreatedAt', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='product',
            name='modifiedAt',
            field=models.DateTimeField(db_column='ModifiedAt', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='createdAt',
            field=models.DateTimeField(db_column='CreatedAt', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='modifiedAt',
            field=models.DateTimeField(db_column='ModifiedAt', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='productrating',
            name='createdAt',
            field=models.DateTimeField(db_column='CreatedAt', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='productrating',
            name='modifiedAt',
            field=models.DateTimeField(db_column='ModifiedAt', default=django.utils.timezone.now),
        ),
    ]
