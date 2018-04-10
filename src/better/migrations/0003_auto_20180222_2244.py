# Generated by Django 2.0.2 on 2018-02-22 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('better', '0002_auto_20180222_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='sport',
            field=models.CharField(choices=[('NCAAF', 'NCAA Football'), ('NCAABB', 'NCAA Baseball'), ('NCAAM', 'NCAA Mens Basketball'), ('NCAAW', 'NCAA Womens Basketball')], default='NCAAF', max_length=100),
        ),
    ]