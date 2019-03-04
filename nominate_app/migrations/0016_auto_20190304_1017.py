# Generated by Django 2.1 on 2019-03-04 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nominate_app', '0015_auto_20190228_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='NominationChain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewed_at', models.DateField(max_length=20)),
            ],
            options={
                'db_table': 'nomination_chains',
            },
        ),
        migrations.CreateModel(
            name='NominationInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('result', models.CharField(max_length=50)),
                ('award_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.AwardTemplate')),
            ],
            options={
                'db_table': 'nomination_instances',
            },
        ),
        migrations.CreateModel(
            name='NominationPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(max_length=20)),
                ('end_date', models.DateField(max_length=20)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.Role')),
                ('nomination_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.NominationPeriod')),
            ],
            options={
                'db_table': 'nomination_plans',
            },
        ),
        migrations.AddField(
            model_name='nominationinstance',
            name='nomination_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.NominationPlan'),
        ),
        migrations.AddField(
            model_name='nominationinstance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.User'),
        ),
        migrations.AddField(
            model_name='nominationchain',
            name='nomination_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.NominationInstance'),
        ),
        migrations.AddField(
            model_name='nominationchain',
            name='reviewer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.User'),
        ),
    ]
