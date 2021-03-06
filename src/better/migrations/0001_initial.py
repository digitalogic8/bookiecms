# Generated by Django 2.0.2 on 2018-02-22 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contestPhoto', models.URLField()),
                ('contest_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamName', models.CharField(max_length=200)),
                ('sport', models.CharField(max_length=200)),
                ('teamPhoto', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='contestant',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='better.Team'),
        ),
        migrations.AddField(
            model_name='contest',
            name='awayTeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awayTeam', to='better.Contestant'),
        ),
        migrations.AddField(
            model_name='contest',
            name='homeTeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeTeam', to='better.Contestant'),
        ),
    ]
