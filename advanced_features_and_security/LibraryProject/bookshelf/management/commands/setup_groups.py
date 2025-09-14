from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = 'Create default groups and assign permissions'

    def handle(self, *args, **kwargs):
        Book = apps.get_model('bookshelf', 'Book')

        # Permissions
        can_view = Permission.objects.get(codename='can_view')
        can_create = Permission.objects.get(codename='can_create')
        can_edit = Permission.objects.get(codename='can_edit')
        can_delete = Permission.objects.get(codename='can_delete')

        # Group: Viewers
        viewers, created = Group.objects.get_or_create(name='Viewers')
        viewers.permissions.set([can_view])

        # Group: Editors
        editors, created = Group.objects.get_or_create(name='Editors')
        editors.permissions.set([can_view, can_create, can_edit])

        # Group: Admins
        admins, created = Group.objects.get_or_create(name='Admins')
        admins.permissions.set([can_view, can_create, can_edit, can_delete])

        self.stdout.write(self.style.SUCCESS("Groups and permissions created successfully."))
