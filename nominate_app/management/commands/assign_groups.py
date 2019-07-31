from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    args = ''
    help = 'Run to create groups and grant permissions'

    def _create_groups(self):
        # add_award = Permission.objects.filter(codename='add_awards')[0]
        permissions = Permission.objects.filter(content_type__app_label='nominate_app')
        group, created = Group.objects.get_or_create(name='Admin', group='level0')
        if created:
            group.permissions.add(*permissions.filter(content_type__model='awards'))

        group, created = Group.objects.get_or_create(name='Manager',  group='level1')
        group, created = Group.objects.get_or_create(name='Technical Jury Member',  group='level2')
        group, created = Group.objects.get_or_create(name='Directorial Board Member',  group='level3')

    def handle(self, *args, **options):
        self._create_groups()