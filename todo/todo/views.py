from todo import models
from django.shortcuts import render,redirect
from .models import Todo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from django.http import HttpResponse


def sign(request):
    if request.method=='POST':
        username=request.POST.get('username','').strip()
        if not username:
            return HttpResponse("Username is required", status=400)
        
        email=request.POST.get('email','').strip()
        if not email:
            return HttpResponse("E-mail is required", status=400)
        password=request.POST.get('password','').strip()

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already in use"}, status=400)
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect ('login/')
    return render(request,'sign.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username','').strip()
        password=request.POST.get('password','').strip()
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user) 
            res = Todo.objects.filter(user=request.user).order_by('-date')
            return render(request,'todo.html', {'res': res})
        else:
            return redirect('todo')
            # return render(request,'login.html')
    return render(request, 'login.html')

def todo(request):
    res = Todo.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        title = request.POST.get('title') 

        if not title:
            return render(request, 'todo.html', {
                'error': 'Title is required',
                'res': Todo.objects.filter(user=request.user).order_by('-date')
            })

        obj = Todo(title=title, user=request.user)
        obj.save()

        return redirect('todo')

    res = Todo.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'todo.html', {'res': res}) 


def edit(request, id):
    obj = Todo.objects.get(id=id)
    print("inside edit")
    if request.method == "POST":
        
        title = request.POST.get('title')
        obj.title= title
        obj.save()
        
        res = Todo.objects.filter(user=request.user).order_by('-date')
        return render(request, 'todo.html', {'res': res})

    res = Todo.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res, 'edit_obj': obj})


def delete(request,id):
    obj=models.Todo.objects.get(id=id) 
    obj.delete()
    return redirect('/todo')

def signout(request):
    logout(request)
    return redirect('/login')