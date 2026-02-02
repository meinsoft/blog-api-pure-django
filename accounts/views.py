from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .decorators import api_login_required
from .utils import *


class RegisterView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):    
        return super().dispatch(request,*args,**kwargs)
    
    def post(self,request):
       
        data,error = parse_json_body(request)

        if(error):
            return error_response("VALIDATION_ERROR",error,status=404)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_two = data.get('password2')

        if(not username or not password):
            return error_response('VALIDATION_ERROR', 'Username and password required', status=400)
        
        if(password!=password_two):
            return error_response('VALIDATION_ERROR', 'Passwords do not match', status=400)
        
        if(User.objects.filter(username=username).exists()):
            return error_response('VALIDATION_ERROR', 'Username already exists', status=400)

        user = User.objects.create_user(username=username,email=email,password=password)
        return JsonResponse({"success": True, "message": "User created","user": {"id": user.id, "username": user.username}}, status=201)

class LoginView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self,request):
        data,error = parse_json_body(request)

        if(error):
            return error_response("VALIDATION_ERROR",error,status=404)

        username = data.get('username')
        password = data.get('password')

        if(not username or not password):
            return error_response('VALIDATION_ERROR', 'Username and password required', status=400)

        user = authenticate(request,username=username,password=password)
        if(user is None):
            return error_response('VALIDATION_ERROR', 'Username is not already exists', status=400)

        login(request,user)
        return JsonResponse({'success': True, 'message': 'Login successful','user': {'id': user.id, 'username': user.username}})

class LogoutView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(api_login_required)
    def post(self,request):
        logout(request)
        return JsonResponse({"success": True, "message": "Logout successful"})

class ShowInformationView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(api_login_required)
    def get(self,request):
        user = request.user
        return JsonResponse({
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })