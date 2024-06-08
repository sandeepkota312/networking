from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from api.models import FriendsNetwork
from networking.forms import CustomUserCreationForm


@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.data)
        print(request.data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                FriendsNetwork.objects.create(user=user)
                login(request, user)
                return Response({'message': 'Signup successful'}, status=200)
            else:
                return Response({'message': 'Signup successful but login failed'}, status=400)
        else:
            return Response({'message': 'Invalid form data','error':form.errors}, status=400)
    else:
        return Response({'message': 'Only POST requests are allowed'}, status=405)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        data = request.data
        email = data.get('email')
        user = User.objects.get(email=email)
        if user:
            username=user.username
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=200)
            else:
                return Response({'message': 'Invalid credentials'}, status=400)
        else:
            return Response({'message': 'Invalid credentials'}, status=400)
    else:
        return Response({'message': 'Only POST requests are allowed'}, status=405)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)
