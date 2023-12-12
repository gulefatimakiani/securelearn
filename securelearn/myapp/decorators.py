from django.http import HttpResponse
from django.shortcuts import redirect




"""
    This decorator will restrict access to manageposts view based on user groups.

    Parameters:
    - allowed_roles (list): A list of role names or group names that are allowed to access the view.
    In this case, the allowed_roles parameter is set to ['admin'].
"""
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group)
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator