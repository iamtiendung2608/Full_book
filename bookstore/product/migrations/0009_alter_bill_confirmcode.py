# Generated by Django 4.0.3 on 2022-04-26 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_rename_cofirmcode_bill_confirmcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='confirmCode',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
