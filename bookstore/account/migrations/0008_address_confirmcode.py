# Generated by Django 4.0.3 on 2022-04-30 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_address_details_alter_address_date_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='confirmCode',
            field=models.CharField(max_length=10, null=True),
        ),
    ]