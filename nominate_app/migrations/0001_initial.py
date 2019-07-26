# Generated by Django 2.2.3 on 2019-07-23 08:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0010_group_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('frequency', models.CharField(choices=[('MONTHLY', 'Monthly'), ('QUATERLY', 'Quaterly'), ('YEARLY', 'Yearly')], max_length=10)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'awards',
                'permissions': (('award_crud', 'can have all the access'),),
            },
        ),
        migrations.CreateModel(
            name='AwardTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.Awards')),
            ],
            options={
                'db_table': 'award_templates',
            },
        ),
        migrations.CreateModel(
            name='NominationInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='new', max_length=50)),
                ('result', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('submitted_at', models.DateTimeField(blank=True, null=True)),
                ('answer_option', models.BooleanField(blank=True, max_length=20, null=True)),
                ('answer_text', models.CharField(blank=True, max_length=500, null=True)),
                ('attachment_path', models.FileField(blank=True, max_length=500, null=True, upload_to='answers/images')),
                ('uploaded_at', models.DateTimeField(blank=True, null=True)),
                ('award_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.AwardTemplate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nomination_instances',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('group', models.CharField(choices=[('level0', 'level0'), ('level1', 'level1'), ('level2', 'level2'), ('level3', 'level3')], max_length=7)),
            ],
            options={
                'db_table': 'roles',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.Role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_roles',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=70, unique=True)),
                ('designation', models.CharField(max_length=70)),
                ('telephonenumber', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('employeenumber', models.CharField(max_length=70)),
                ('jobtitle', models.CharField(max_length=70)),
                ('cn', models.CharField(max_length=70)),
                ('title', models.CharField(max_length=70)),
                ('lastpwdchange', models.CharField(max_length=70)),
                ('defaultpwd', models.CharField(max_length=70)),
                ('baselocation', models.CharField(max_length=70)),
                ('uid', models.CharField(max_length=70)),
                ('worklocation', models.CharField(max_length=70)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profiles',
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qname', models.CharField(max_length=100)),
                ('qtype', models.CharField(choices=[('SUBJECTIVE', 'subjective'), ('OBJECTIVE', 'objective')], default='subjective', max_length=100)),
                ('attachment_need', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('award_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.AwardTemplate')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'db_table': 'award_questions',
            },
        ),
        migrations.CreateModel(
            name='NominationTimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.DateField(max_length=20)),
                ('end_day', models.DateField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.Awards')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('nomination_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.NominationInstance')),
            ],
            options={
                'db_table': 'nomination_time_slots',
            },
        ),
        migrations.CreateModel(
            name='NominationSubmitter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewed_at', models.DateField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('submit_later', models.IntegerField(choices=[('SAVE', 1), ('SUBMIT', 0)], default=0)),
                ('nomination_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.NominationInstance')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nomination_submitters',
            },
        ),
        migrations.CreateModel(
            name='NominationPeriodFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.DateField(max_length=20)),
                ('end_day', models.DateField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.Awards')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'db_table': 'nomination_period_frequency',
            },
        ),
        migrations.CreateModel(
            name='NominationPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.DateField(max_length=20)),
                ('end_day', models.DateField(max_length=20)),
                ('is_template', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.Awards')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'db_table': 'nomination_periods',
            },
        ),
        migrations.CreateModel(
            name='NominationAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(blank=True, null=True)),
                ('answer_option', models.BooleanField(blank=True, max_length=20, null=True)),
                ('answer_text', models.CharField(blank=True, max_length=500, null=True)),
                ('attachment_path', models.FileField(blank=True, max_length=500, null=True, upload_to='answers/images')),
                ('uploaded_at', models.DateTimeField(blank=True, null=True)),
                ('award_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.AwardTemplate')),
                ('nomination_chain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.NominationSubmitter')),
                ('nomination_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.NominationInstance')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nominate_app.Questions')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nomination_answers',
            },
        ),
    ]
