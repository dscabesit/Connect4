# Generated by Django 3.1.1 on 2020-09-24 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name1', models.CharField(max_length=50)),
                ('name2', models.CharField(max_length=50)),
                ('mat', models.CharField(max_length=100)),
            ],
        ),
    ]
