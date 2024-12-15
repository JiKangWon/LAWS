from django.shortcuts import render
from .models import *

# Create your views here.
def get_home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username=username, password=password)
        user_inf = UserInfo.objects.get(user=user)
        context = {
            'user':user,
            'user_inf': user_inf,  
        }
        if user:
            return render(request, 'page/home.html', context)
    return render(request, 'log/login.html')