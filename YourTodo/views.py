from YourTodo.models import Todo
from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ToDoForms,UserRegistrationForm
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, timedelta
from django.contrib import messages


def Done(request):
    if request.user.is_authenticated:
        donetask=Todo.objects.filter(user=request.user,Isdone=True)
    else:
       donetask=''
    
    text=ToDoForms()
    return render(request,'Home/index.html',{'TodoList':donetask,'Formdata':text})
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            subject=f"New message from {name}",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["afsheentahir0011@gmail.com"],
        )
        return render(request, "contact.html", {"success": True})
    return render(request, "contact.html")

def Home(request):
    if request.user.is_authenticated:
       todo=Todo.objects.filter(user=request.user,Isdone=False)
    else:
        todo=request.session.get("guest_todos",[])
    today=date.today()
    tomorrow=today+timedelta(days=1)
    if request.user.is_authenticated:
     due_soon=todo.filter(due_date=tomorrow)
     due_today=todo.filter(due_date=today)

     if due_soon.exists():
        for task in due_soon:
         
          messages.warning(request,  f"Task '{task.Title}' is due tomorrow!⚠️")
     if due_today.exists():
        for task in due_today:
          
          messages.warning(request,  f"Task '{task.Title}' is due Today!⚠️")
    text=ToDoForms()
    
    return render(request,'Home/index.html',{'TodoList':todo,'Formdata':text})
def Detail(request):
    
    return render(request,'Detail/index.html')
@login_required
def Delete(request,id):
    todo_delete=get_object_or_404(Todo, pk=id,user=request.user )
    if todo_delete.Isdone==True:
      todo_delete.delete()
      return redirect('Done')
    else:
       todo_delete.delete()
       return redirect('Home')

def Add(request):
    
    if request.method=='POST':
       formAdd=ToDoForms(request.POST)
       if formAdd.is_valid():
          if request.user.is_authenticated:
           todo= formAdd.save(commit=False)
           todo.user=request.user
           todo.save()
          else:
             guest_todos=request.session.get("guest_todos",[])
             guest_id_counter = request.session.get("guest_id_counter", 0)
             guest_id_counter += 1
             request.session["guest_id_counter"] = guest_id_counter
             guest_todo = {
                    "id": guest_id_counter,
                    "Title": formAdd.cleaned_data["Title"],
                    "Description": formAdd.cleaned_data.get("Description", ""),
                    "Isdone": False,
                }
             guest_todos.append(guest_todo)
             request.session["guest_todos"] = guest_todos
             request.session.modified = True
          return redirect('Home')
    else:
      formAdd=ToDoForms()
    if request.user.is_authenticated:
     todos=Todo.objects.filter(user=request.user)
    else:
       todos=request.session.get("guest_todos",[])
    return render(request,'Home/index.html',{'Formdata':formAdd,'TodoList':todos})
@login_required
def Update(request, id):
    todos = get_object_or_404(Todo, pk=id,user=request.user)

    if request.method == 'POST':
        formEdit = ToDoForms(request.POST, instance=todos)
        
        if formEdit.is_valid():
            todos = formEdit.save(commit=False) 
            todos.user = request.user
           
            todos.save()
            
            return redirect('Home') 
    else:
        formEdit = ToDoForms(instance=todos)
    return render(request, 'Update/index.html', {'TodoList': formEdit})

def registration(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
           user=form.save(commit=False)
           user.set_password(form.cleaned_data['password1'])
           user.save()
           login(request,user)
           return redirect('Home')
    else:
        form=UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def Login(request):
   if request.method=="POST":
      form=AuthenticationForm(request,data=request.POST)
      if form.is_valid():
         username=form.cleaned_data.get('username')
         password=form.cleaned_data.get('password')
         user=authenticate(request,username=username,password=password)
         if user is not None:
            login(request,user)
            return redirect('Home')
   else:
            form=AuthenticationForm()
   return render(request,'registration/login.html',{'form':form})

      
def Logout(request):
   if request.method=='POST':
      logout(request)
      return redirect('Home')
   

