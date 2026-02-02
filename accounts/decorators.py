from functools import wraps
from django.http import JsonResponse

def api_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if(request.user.is_authenticated):
        	return func(request,*args,**kwargs)
        else:
        	return JsonResponse({
                'success': False,
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Login required'
                }
            }, status=401)
    return wrapper