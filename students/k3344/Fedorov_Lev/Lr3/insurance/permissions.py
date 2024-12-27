from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Contract, Employee, Organization


def create_roles_and_permissions():
    agency_admin_group, _ = Group.objects.get_or_create(name='AgencyAdmin')
    company_director_group, _ = Group.objects.get_or_create(name='CompanyDirector')

    contract_content_type = ContentType.objects.get_for_model(Contract)
    employee_content_type = ContentType.objects.get_for_model(Employee)
    organization_content_type = ContentType.objects.get_for_model(Organization)

    permissions = [
        ('view_contract', 'Can view contract', contract_content_type),
        ('add_contract', 'Can add contract', contract_content_type),
        ('change_contract', 'Can change contract', contract_content_type),
        ('delete_contract', 'Can delete contract', contract_content_type),

        ('view_employee', 'Can view employee', employee_content_type),
        ('add_employee', 'Can add employee', employee_content_type),
        ('change_employee', 'Can change employee', employee_content_type),
        ('delete_employee', 'Can delete employee', employee_content_type),

        ('view_organization', 'Can view organization', organization_content_type),
        ('change_organization', 'Can change organization', organization_content_type),
    ]

    for codename, name, content_type in permissions:
        perm, _ = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=content_type,
        )

        # Назначаем права группам
        if 'contract' in codename or 'employee' in codename:
            company_director_group.permissions.add(perm)

        if 'approve' in codename or 'reject' in codename:
            company_director_group.permissions.add(perm)

        if 'organization' in codename:
            agency_admin_group.permissions.add(perm)

    print("Roles and permissions successfully created.")