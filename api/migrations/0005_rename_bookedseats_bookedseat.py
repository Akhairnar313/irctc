# Generated by Django 4.2.3 on 2023-07-10 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_boooking_id_bookedseats_boooking_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookedSeats',
            new_name='BookedSeat',
        ),
    ]