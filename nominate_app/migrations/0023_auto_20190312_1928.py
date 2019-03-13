# Generated by Django 2.1 on 2019-03-12 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nominate_app', '0022_auto_20190312_0744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nominationinstance',
            name='nomination_plan',
        ),
        migrations.AddField(
            model_name='nominationinstance',
            name='nomination_period',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='nominate_app.NominationPeriod'),
            preserve_default=False,
        ),
    ]
