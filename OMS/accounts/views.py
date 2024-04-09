import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q, F, Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import *
from .forms import OrderForm, CreateUserForm, UpdateUserForm
from .orderFilters import OrderFilter
from .userFilters import UserFilter
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='worker'))  # Add user to 'worker' group
            messages.success(request, 'Account was created for ' + user.username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):

        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else: 
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

####DASHBOARD####

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'manager', 'worker'])
def home(request):
    orders = Order.objects.all()

    total_pending = orders.exclude(status='Complete').count()
    urgent = orders.filter(priority='Urgent').exclude(status='Complete').count()
    regular = orders.filter(priority='Normal').exclude(status='Complete').count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'orders': orders ,
                'total_pending': total_pending,
                'urgent': urgent,
                'regular': regular,
                'myFilter': myFilter
                }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def viewOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    comments = Comment.objects.filter(order=order)
    context = {'order': order,
                'comments': comments  
              }

    return render(request, "accounts/view_order.html", context)


@login_required(login_url='login')
def createOrder(request):
    response = requests.get('https://covid-api.com/api/regions').json()
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {"form": form,
                "response": response
    }
    return render(request, "accounts/order_form.html", context)
    
@login_required(login_url='login')
def searchOrder(request):
    search_query = request.GET.get("search_query")
    if search_query:
        if search_query.isdigit():
            orders = Order.objects.filter(Q(id=int(search_query)) | Q(title__icontains=search_query))
        else: 
            orders = Order.objects.filter(title__icontains=search_query)
    else:
        orders = Order.objects.all()

    context = {"orders": orders, "search_query": search_query}

    return render(request, "accounts/dashboard.html", context)


@login_required(login_url='login')
def addComment(request, pk):
    current_order = get_object_or_404(Order, pk=pk)
    current_username = request.user
    current_date = datetime.now()
    new_comment = Comment(
        comment_text = request.POST["comment_text"],
        order = current_order,
        user = current_username,
        date_created = current_date
    )
    new_comment.save()

    return redirect('view_order', pk=pk)


@login_required(login_url='login')
def deleteComment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

   
    if request.user == comment.user:
        comment.delete()

        return redirect('view_order', pk=comment.order.pk)
    else:

        return HttpResponse("You are not authorized to delete this comment.")
        

@login_required(login_url='login')
def updateOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete_order.html', context)


####USERS#####

@login_required(login_url='login')
def userListPage(request):
    admin_group = Group.objects.get(name='admin')

    users = User.objects.order_by('-date_joined')

    myFilter = UserFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {'users': users,
                'myFilter': myFilter
                }

    return render(request, 'accounts/users.html', context)


@login_required(login_url='login')
def viewUser(request, pk):
    user = get_object_or_404(User, pk=pk)
    groups = user.groups.all()
    context = {'user': user, 'groups': groups}

    return render(request, 'accounts/view_user.html', context)
    

@login_required(login_url='login')
def createUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users')
    
    context = {"form": form}

    return render(request, 'accounts/user_form.html', context)

@login_required(login_url='login')
def updateUser(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            selected_roles = form.cleaned_data.get('groups')
            print("Selected roles:", selected_roles)
            form.save()
            return redirect('view_user', pk=pk)

    context = {'form': form}
    return render(request, 'accounts/update_user_form.html', context)


@login_required(login_url='login')
def deleteUser(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user.is_superuser:
        messages.error(request, "Cannot delete superuser.")
        return redirect('users')

    if request.method == "POST":
        user.delete()
        return redirect('users')

    context = {'user': user}
    return render(request, 'accounts/delete_user.html', context)

@login_required(login_url='login')
def reports(request):
    orders = Order.objects.all()

    orders_created = orders.count()
    orders_pending = orders.exclude(status='Complete').count()
    orders_urgent = orders.filter(priority='Urgent').exclude(status='Complete').count()
    orders_normal = orders.filter(priority='Normal').exclude(status='Complete').count()
    orders_attention_required = orders.filter(status='Attention Required').count()
    orders_completed = orders.filter(status='Complete').count()

    users = User.objects.all()
    users_created = users.count()

    context = {'orders_created': orders_created,
                'orders_pending': orders_pending,
                'orders_urgent': orders_urgent,
                'orders_normal': orders_normal,
                'orders_attention_required': orders_attention_required,
                'orders_completed': orders_completed,
                'users_created': users_created,
                }

    return render(request, 'accounts/reports.html', context)
