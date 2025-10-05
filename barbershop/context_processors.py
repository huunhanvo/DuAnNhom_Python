"""
Context processors for barbershop application
"""

def user_context(request):
    """Add user information to template context"""
    user_info = {}
    
    if 'user_id' in request.session:
        user_info = {
            'id': request.session.get('user_id'),
            'ho_ten': request.session.get('ho_ten', ''),
            'vai_tro': request.session.get('vai_tro', ''),
        }
    
    return {'user': user_info}