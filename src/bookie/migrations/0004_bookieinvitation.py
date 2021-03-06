# Generated by Django 2.0.4 on 2018-07-11 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookie', '0003_auto_20180711_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookieInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitedEmail', models.EmailField(max_length=254)),
                ('filled', models.BooleanField()),
                ('bookie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookie.BookieProfile')),
            ],
        ),
    ]
