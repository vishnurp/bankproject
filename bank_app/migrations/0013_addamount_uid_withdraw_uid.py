# Generated by Django 4.2.1 on 2023-07-18 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0012_newsmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='addamount',
            name='uid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='withdraw',
            name='uid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
