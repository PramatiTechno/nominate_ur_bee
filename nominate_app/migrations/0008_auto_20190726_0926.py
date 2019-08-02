# Generated by Django 2.2.3 on 2019-07-26 09:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nominate_app', '0007_merge_20190726_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='options',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=20),
        ),
    ]