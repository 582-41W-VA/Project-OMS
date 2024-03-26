from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    orders = get_object_or_404(Order, pk=pk)
    context = {'orders': orders}

    return render(request, "accounts/view_order.html", context)


@login_required(login_url='login')
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {"form": form}
    return render(request, "accounts/order_form.html", context)


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
            selected_roles = form.cleaned_data.get('groups')  # Get selected roles
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