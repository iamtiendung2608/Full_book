# Generated by Django 4.0.3 on 2022-05-07 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_alter_bill_date_created'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together={('id', 'date_created')},
        ),
    ]
