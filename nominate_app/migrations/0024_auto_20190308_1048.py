# Generated by Django 2.1 on 2019-03-08 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nominate_app', '0023_auto_20190308_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nominationanswers',
            name='attachment_path',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to=''),
        ),
    ]
