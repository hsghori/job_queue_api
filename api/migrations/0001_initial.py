# Generated by Django 2.2.8 on 2019-12-13 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('url', models.URLField(db_index=True)),
                ('result', models.TextField(null=True)),
                ('status', models.CharField(choices=[('Q', 'QUEUED'), ('C', 'COMPLETE'), ('F', 'FAILED')], max_length=1)),
                ('time_created', models.DateTimeField()),
                ('time_updated', models.DateTimeField(null=True)),
            ],
        ),
    ]
