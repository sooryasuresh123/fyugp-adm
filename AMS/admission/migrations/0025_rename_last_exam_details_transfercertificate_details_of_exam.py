# Generated by Django 5.1.7 on 2025-03-13 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0024_alter_transfercertificate_date_of_admission_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfercertificate',
            old_name='last_exam_details',
            new_name='details_of_exam',
        ),
    ]
