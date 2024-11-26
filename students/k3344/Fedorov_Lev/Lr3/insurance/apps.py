from django.apps import AppConfig
from django.db.models.signals import post_migrate


class InsuranceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'insurance'

    def ready(self):
        post_migrate.connect(create_default_groups_and_permissions, sender=self)


def create_default_groups_and_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from .models import Contract, Employee

    groups_permissions = {
        'Agent': ['add_contract', 'change_contract', 'view_contract'],
        'Employee': ['view_contract'],
        'Organization Admin': ['add_employee', 'change_employee', 'view_employee'],
    }

    for group_name, permissions in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for perm in permissions:
            try:
                content_type = ContentType.objects.get(app_label='insurance', model=perm.split('_')[1])
                permission = Permission.objects.get(content_type=content_type, codename=perm)
                group.permissions.add(permission)
            except ContentType.DoesNotExist:
                print(f"ContentType for {perm.split('_')[1]} not found!")
            except Permission.DoesNotExist:
                print(f"Permission {perm} not found!")
