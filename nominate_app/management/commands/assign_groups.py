from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User

class Command(BaseCommand):
    args = ''
    help = 'Run to create groups and grant permissions'

    def _create_groups(self):

        add_award = Permission.objects.filter(codename='add_awards')[0]

        group, created = Group.objects.get_or_create(name='admin')
        if created:
            group.permissions.add(add_award)
            # logger.info('admin Group created')

        group, created = Group.objects.get_or_create(name='Manager')
        group, created = Group.objects.get_or_create(name='Technical Jury Member')
        group, created = Group.objects.get_or_create(name='Directorial Board Member')

    def handle(self, *args, **options):
        self._create_groups()