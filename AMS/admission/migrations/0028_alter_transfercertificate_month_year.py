# Generated by Django 5.1.7 on 2025-03-13 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0027_alter_transfercertificate_month_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfercertificate',
            name='month_year',
            field=models.CharField(max_length=7),
        ),
    ]
