# Generated by Django 2.1 on 2019-02-25 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nominate_app', '0010_auto_20190225_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awards',
            name='frequency',
            field=models.CharField(choices=[('M', 'Monthly'), ('Q', 'Quaterly'), ('Y', 'Yearly')], max_length=3),
        ),
        migrations.AlterField(
            model_name='awards',
            name='name',
            field=models.CharField(default='NULL', max_length=30),
            preserve_default=False,
        ),
    ]
