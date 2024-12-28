from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from .models import HotelBaseAccount

if __name__ == "__main__":
    content_type = ContentType.objects.get_for_model(HotelBaseAccount)
    table_permission = Permission.objects.create(codename='can_see_residents_table',
                                                 name='Can see table of residents for last month',
                                                 content_type=content_type)

    admins_group = Group.objects.create(name='Admins Group')
    admins_group.permissions.add(table_permission)