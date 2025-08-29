from django.conf import settings

""" check superadmin role """
def user_role_super_admin(user):
    return user.group.id == settings.GRP_SUPER_ADMIN


def is_superuser(user):
    return user.role == 1   

def is_staff(user):
    return user.role == 2