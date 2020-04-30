from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

##################################### User auth ####################

def register(request):
    if request.method == "POST":
        # User has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/register.html',{'error1':'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                return redirect('login')
        else:
            return render(request, 'accounts/register.html', {'error2': 'Passwords must match'})

    else:
        # User wants to enter info
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html',{'error':'username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('home')

##################################################

@login_required(login_url='login')
def home(request):
    dataset = Dataset.objects.all()
    context ={
        'dataset': dataset
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')
def create(request):
    form = DatasetForm()
    if request.method == "POST":
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'create.html', context)

@login_required(login_url='login')
def update(request, pk):
    data = Dataset.objects.get(id=pk) # id
    form = DatasetForm(instance=data) # hare you can see you previous data.
    if request.method == "POST":
        form = DatasetForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()

    context = {
        'data': data,
        'form': form
    }
    return render(request, 'update.html', context)

@login_required(login_url='login')
def delete(request, pk):
    data = Dataset.objects.get(id=pk)
    if request.method == "POST":
        data.delete()
        return redirect('home')

    context = {
        'item': data
    }
    return render(request, 'delete.html', context)


