# Generated by Django 4.2.1 on 2023-07-06 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0008_withdraw'),
    ]

    operations = [
        migrations.DeleteModel(
            name='withdraw',
        ),
        migrations.AddField(
            model_name='regmodel',
            name='withdraw_amt',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
