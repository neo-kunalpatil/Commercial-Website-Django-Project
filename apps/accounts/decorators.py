from django.core.exceptions import PermissionDenied

def seller_required(function):
    """
    Decorator for views that checks that the user is logged in
    and has the SELLER role, raising PermissionDenied otherwise.
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seller:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
