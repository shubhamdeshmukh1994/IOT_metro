# Generated by Django 2.0.3 on 2018-04-10 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biometric_ticket', '0006_auto_20180410_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
