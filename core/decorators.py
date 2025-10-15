"""
Authentication decorators for barbershop application
"""
from django.shortcuts import redirect


def require_auth(view_func):
    """Decorator to require authentication"""
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            # Check role to redirect appropriately
            return redirect('accounts:customer_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def require_role(allowed_roles):
    """Decorator to require specific role"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if 'user_id' not in request.session:
                # Staff/Admin should go to staff login
                if any(role in allowed_roles for role in ['nhan_vien', 'quan_ly']):
                    return redirect('accounts:staff_login')
                # Customer should go to customer login
                return redirect('accounts:customer_login')
            user_role = request.session.get('vai_tro')
            if user_role not in allowed_roles:
                # Redirect based on required role
                if any(role in allowed_roles for role in ['nhan_vien', 'quan_ly']):
                    return redirect('accounts:staff_login')
                return redirect('accounts:customer_login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
