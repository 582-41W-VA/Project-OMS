from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import OrderForm, CreateUserForm
from .orderFilters import OrderFilter
from .userFilters import UserFilter
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def registerPage(request):

        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
def userListPage(request):
    users = User.objects.all()

    myFilter = UserFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {'users': users,
                'myFilter': myFilter
                }

    return render(request, 'accounts/users.html', context)


@login_required(login_url='login')
def order(request, pk):
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

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

