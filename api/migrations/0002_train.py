# Generated by Django 4.2.3 on 2023-07-10 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_name', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('seat_capacity', models.IntegerField()),
                ('arrival_time_at_source', models.DateTimeField()),
                ('arrival_time_at_destination', models.DateTimeField()),
            ],
        ),
    ]
