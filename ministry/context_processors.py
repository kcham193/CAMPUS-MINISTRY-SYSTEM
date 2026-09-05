from .permissions import is_admin


def user_role(request):
    return {'is_admin': is_admin(request.user)}