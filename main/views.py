import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta
from .models import *

# Create your views here.
@login_required(login_url='log_in')
def index(request):
    count=Assign_task.objects.filter(is_deleted=False, is_completed=False,assigned_by=request.user).count()
    completed_count=Task.objects.filter(is_completed=True, is_deleted=False, user=request.user).count()
    current_count=Task.objects.filter(is_completed=False, is_deleted=False, user=request.user).count()
    return render(request, 'main/index.html',{'count':count,'completed_count':completed_count,'current_count':current_count})

def base(request):
    return render(request,'base.html',{'user_name':request.user})

def log_in(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username is not registered.')
            return redirect('log_in')
        user=authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(1200000)
            else:
                request.session.set_expiry(0)
            messages.success(request,"Login successfully!")
            return redirect('index')
        else:
            messages.error(request,"Invalid password")
            return redirect('log_in')
            
    return render(request,'auth/login.html')
    
def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password1=request.POST['password1']

        if password==password1:
            try:
                 validate_password(password)
                 if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                    return redirect('register')
                 elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('register')
                 elif username.lower() in password.lower():
                     messages.error(request,"Password cannot be too similar to username.")
                     return redirect('register')
                 elif not re.search(r'[A-Z]',password):
                    messages.error(request,"Password must contain atleast one uppercase letter.")
                    return redirect('register')
                 elif not re.search(r'\d', password):
                     messages.error(request, "Password must contain atleast one digit.")
                     return redirect('register')
                 elif not re.search(r'[@#%$<>]', password):
                     messages.error(request, "Password must contain atleast one special character.")
                     return redirect('register')
                 
                 else:
                   User.objects.create_user(first_name=first_name, last_name=last_name,email=email,username=username,password=password)
                   messages.success(request, "Registered successfully!")
                   return redirect('log_in')
                 
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')

           
        else:
            messages.error(request,"Your passwords doesn't match")
            return redirect('register')

    return render(request,'auth/register.html')

def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')

    return render(request, 'auth/change_password.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('log_in')


def create_task(request):
    if request.method=='POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get ('status')
        start_date = request.POST.get( 'start_date')
        end_date = request.POST.get('end_date')
        user=request.user

        create=Task.objects.create(title=title, description=description, status=status, start_date=start_date, end_date=end_date, user=user)
        messages.success(request,"Your task has been created successfully!")
        create.save()
        return redirect('index')
    return render(request, 'main/create_task.html')

def assign_task(request):
    
    if request.method=='POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get ('status')
        username=request.POST.get('user')
        due_date = request.POST.get('due_date')
        assigned_by = request.user

        if User.objects.filter(username=username).exists():
           user1=User.objects.get(username=username)#to whom task is assigned
           user2=User.objects.get(username=assigned_by)#user assigning the task

           assign=Assign_task.objects.create(title=title, description=description, status=status, assign_to=user1,due_date=due_date, assigned_by=user2)
           assign.save()
           messages.success(request, "Task has been successfully assigned!")
           return redirect('index')
        else:
            messages.error(request, "Username doesnot exists!")
            return redirect('assign')
    return render(request, 'main/assign_task.html')

# -----view task section----#
def view_task(request):
    search=request.GET.get('search')
    if search:
        data=Task.objects.filter(title__icontains=search)
    else:
        data=Task.objects.filter(is_deleted=False,is_completed=False)
        sort_by=None
        if request.method == 'POST':
          sort_by=request.POST.get('sort_by')
        if sort_by:
            sort_by = sort_by.strip() 
            data=data.order_by(sort_by)
    return render(request, 'main/view.html',{'data':data})

def edit(request,id):
    data=Task.objects.get(id=id)
    if request.method=='POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get ('status')
        start_date = request.POST.get( 'start_date')
        end_date = request.POST.get('end_date')

        data=Task.objects.get(id=id)

        data.title=title
        data.description=description
        data.status=status
        data.start_date=start_date
        data.end_date=end_date
        data.save()
        return redirect('view_task')
    return render(request, 'main/edit.html', {'data':data})

def delete_data(request,id):
    data=Task.objects.get(id=id)
    data.is_deleted = True
    data.delete_time=datetime.now()
    data.save()
    return redirect('view_task')

def clear_data(request):
    Task.objects.all().update(is_deleted=True)
    return redirect('view_task')
#------view task section ends----#

#-----recycle section starts----#
def recycle(request):
    data=Task.objects.filter(is_deleted=True)
    # time = datetime.now()-timedelta(days=30)
    # time1=Task.objects.filter(delete_time__lt=time)
    # time1.delete()
    return render(request,'main/recycle.html',{'data':data})

def restore(request,id):
    data=Task.objects.get(id=id)
    data.is_deleted= False
    data.save()
    messages.success(request,"Your data has been restored successfully!")
    return redirect('recycle')
#------recycle section ends----#

# ----Assigned task-----#
def assigned_task(request):
    data=Assign_task.objects.filter(is_completed=False)

    return render(request,'main/assigned_task.html',{'data':data})
# ---assigned task mark as completed---#

def completed(request,id):
    data=Assign_task.objects.get(id=id)
    data.is_completed=True
    data.save()
    messages.success(request,"Your task has been marked completed!")
    return redirect('assigned_task')

#---current task mark as completd---#
def current_completed(request,id):
    current_completed=Task.objects.get(id=id)
    current_completed.is_completed=True
    current_completed.save()
    messages.success(request,"Your task has been marked completed!")
    return redirect('view_task')

#----completed page----#
def completed_tasks(request):
    assign_data=Assign_task.objects.filter(is_completed=True,is_deleted=False)
    current_data=Task.objects.filter(is_completed=True, is_deleted=False)
    
    return render(request, 'main/completed_task.html',{'data1':assign_data,'data2':current_data})
 
def delete_assign(request,id):
    assign_delete=Assign_task.objects.get(id=id)
    assign_delete.is_deleted=True
    assign_delete.delete_time=datetime.now()
    assign_delete.save()
    return redirect('completed_tasks')

def delete_current(request,id):
    current_delete=Task.objects.get(id=id)
    current_delete.is_deleted=True
    current_delete.delete_time=datetime.now()
    current_delete.save()
    return redirect('completed_tasks')
