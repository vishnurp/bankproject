# Generated by Django 4.2.1 on 2023-07-03 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0003_regmodel_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regmodel',
            name='pin',
            field=models.IntegerField(max_length=4),
        ),
    ]