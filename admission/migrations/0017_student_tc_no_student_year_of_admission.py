# Generated by Django 5.1.7 on 2025-03-10 14:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0016_delete_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='tc_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admission.transfercertificate'),
        ),
        migrations.AddField(
            model_name='student',
            name='year_of_admission',
            field=models.IntegerField(default='2025'),
        ),
    ]
