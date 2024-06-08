from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Signup successful'}, status=200)
            else:
                return Response({'message': 'Signup successful but login failed'}, status=400)
        else:
            return Response({'message': 'Invalid form data'}, status=400)
    else:
        return Response({'message': 'Only POST requests are allowed'}, status=405)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=200)
        else:
            return Response({'message': 'Invalid credentials'}, status=400)
    else:
        return Response({'message': 'Only POST requests are allowed'}, status=405)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)
