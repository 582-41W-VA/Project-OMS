"""
Module Docstring:

This module contains views and functions for managing user authentication, order management,
user management, and generating reports in a web application.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Order, Comment, User
from .forms import OrderForm, CreateUserForm, UpdateUserForm
from .orderFilters import OrderFilter
from .userFilters import UserFilter
from .decorators import unauthenticated_user, allowed_users


# REGISTER
@unauthenticated_user
def registerPage(request):
    """
    View function for registering a new user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the request method is 'GET', renders the registration form page.
    - If the request method is 'POST':
        - If the form data is valid and a new user is successfully created:
            - Adds the user to the 'worker' group by default.
            - Displays a success message.
            - Redirects the user to the login page.
        - If the form data is invalid or an error occurs during user creation:
            - Re-renders the registration form page with error messages.
    """
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name="worker"))
            messages.success(request, "Account was created for " + user.username)
            return redirect("login")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


# LOGIN
@unauthenticated_user
def loginPage(request):
    """
    View function for handling user login.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the request method is 'GET', renders the login page.
    - If the request method is 'POST':
        - Attempts to authenticate the user with the provided username and password.
        - If authentication is successful, logs the user in and redirects to the home page.
        - If authentication fails, displays an error message and re-renders the login page.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.info(request, "Username OR password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


# LOGOUT
def logoutUser(request):
    """
    View function for handling user logout.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Redirects the user to the login page after logging them out.
    """
    logout(request)
    return redirect("login")


####DASHBOARD####
# HOME
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "manager", "worker"])
def home(request):
    """
    View function for the home page/dashboard.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Renders the dashboard template with the appropriate context data:
        * orders: All orders queryset.
        * total_pending: Total count of pending orders.
        * urgent: Count of urgent orders.
        * regular: Count of regular (non-urgent) orders.
        * myFilter: The order filter instance.
        * page_title: Title of the dashboard page.
    """
    orders = Order.objects.all()

    total_pending = orders.exclude(status="Complete").count()
    urgent = orders.filter(priority="Urgent").exclude(status="Complete").count()
    regular = orders.filter(priority="Normal").exclude(status="Complete").count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        "orders": orders,
        "total_pending": total_pending,
        "urgent": urgent,
        "regular": regular,
        "myFilter": myFilter,
        "page_title": "Dashboard",
    }

    return render(request, "accounts/dashboard.html", context)


# VIEW ORDER
@login_required(login_url="login")
def viewOrder(request, pk):
    """
    View function for displaying details of a specific order.

    Parameters:
    - request: The HTTP request object.
    - pk: The primary key of the order to be viewed.

    Returns:
    - Renders the view order template with the appropriate context data:
        * order: The order object to be viewed.
        * comments: Comments associated with the order.
        * qr_code_url: URL for the QR code image.
    """
    order = get_object_or_404(Order, pk=pk)
    comments = Comment.objects.filter(order=order).order_by("-date_created")

    base_url = request.build_absolute_uri("/").rstrip("/")
    path = request.get_full_path()
    qr_data = base_url + path
    qr_code_url = (
        f"http://api.qrserver.com/v1/create-qr-code/?data={qr_data}&size=100x100"
    )

    context = {
        "order": order,
        "comments": comments,
        "qr_code_url": qr_code_url,
        "page_title": "View Order",
    }

    return render(request, "accounts/view_order.html", context)


# CREATE ORDER
@login_required(login_url="login")
def createOrder(request):
    """
    View function for creating a new order.

    If the request method is POST, processes the submitted form data
    to create a new order. Redirects to the home page after successful
    form submission.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Renders the order form template with the appropriate context data:
        * form: An instance of the OrderForm for creating a new order.
        * page_title: Title for the page.
    """
    form = OrderForm()

    workers_group = Group.objects.filter(name="worker").first()
    workers = workers_group.user_set.all()

    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")

    form.fields["order_assigned_to"].queryset = workers

    context = {"form": form, "page_title": "Create Order"}

    return render(request, "accounts/order_form.html", context)


# SEARCH ORDER
@login_required(login_url="login")
def searchOrder(request):
    """
    View function for searching orders.

    Retrieves the search query from the request's GET parameters.
    If a search query is provided, filters the orders based on whether
    the query is a number (searching by order ID) or a string (searching by title).
    If no search query is provided, retrieves all orders.
    Renders the dashboard template with the search results and search query.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Renders the dashboard template with the following context data:
        * orders: A queryset of orders filtered based on the search query.
        * search_query: The search query entered by the user.
        * page_title: Title for the page.
    """
    search_query = request.GET.get("search_query")
    if search_query:
        if search_query.isdigit():
            orders = Order.objects.filter(
                Q(id=int(search_query)) | Q(title__icontains=search_query)
            )
        else:
            orders = Order.objects.filter(title__icontains=search_query)
    else:
        orders = Order.objects.all()

    context = {"orders": orders, "search_query": search_query, "page_title": "Orders"}

    return render(request, "accounts/dashboard.html", context)


# ADD COMMENT
@login_required(login_url="login")
def addComment(request, pk):
    """
    View function for adding a comment to an order.

    Retrieves the current order based on the provided primary key (pk) from the URL.
    Retrieves the current user's username and the current date and time.
    Creates a new Comment object with the provided comment text, current order,
    current user, and current date and time.
    Saves the new comment to the database.
    Redirects the user to the view order page for the same order.

    Parameters:
    - request: The HTTP request object.
    - pk: The primary key of the order to which the comment will be added.

    Returns:
    - Redirects to the view order page for the specified order (pk).
    """
    current_order = get_object_or_404(Order, pk=pk)
    current_username = request.user
    current_date = datetime.now()
    new_comment = Comment(
        comment_text=request.POST["comment_text"],
        order=current_order,
        user=current_username,
        date_created=current_date,
    )
    new_comment.save()

    return redirect("view_order", pk=pk)


# DELETE COMMENT
@login_required(login_url="login")
def deleteComment(request, comment_id):
    """
    View function for deleting a comment.

    Retrieves the comment object based on the provided comment_id from the URL.
    Checks if the current user is a superuser or the owner of the comment.
    If authorized, deletes the comment from the database and redirects to the
    view order page for the corresponding order.
    If not authorized, returns an HTTP response indicating lack of authorization.

    Parameters:
    - request: The HTTP request object.
    - comment_id: The primary key of the comment to be deleted.

    Returns:
    - Redirects to the view order page for the corresponding order if authorized.
    - HTTP response indicating lack of authorization if not authorized.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user.is_superuser or request.user == comment.user:
        comment.delete()
        return redirect("view_order", pk=comment.order.pk)

    return HttpResponse("You are not authorized to delete this comment.")


# UPDATE ORDER
@login_required(login_url="login")
def updateOrder(request, pk):
    """
    View function for updating an existing order.

    Retrieves the order object based on the provided pk (primary key) from the URL.
    Initializes an OrderForm instance with the retrieved order data.
    If the request method is POST, processes the form data submitted by the user.
    If the form is valid, saves the updated order to the database.
    Redirects to the home page after successful form submission.

    Parameters:
    - request: The HTTP request object.
    - pk: The primary key of the order to be updated.

    Returns:
    - Redirects to the home page after successful form submission.
    """
    order = get_object_or_404(Order, pk=pk)

    workers_group = Group.objects.filter(name="worker").first()
    workers = workers_group.user_set.all()

    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = OrderForm(instance=order)
        form.fields["order_assigned_to"].queryset = workers

    context = {"form": form, "order": order, "page_title": "Update Order"}
    return render(request, "accounts/update_order_form.html", context)


# DELETE ORDER
@login_required(login_url="login")
def deleteOrder(request, pk):
    """
    View function for deleting an existing order.

    Retrieves the order object based on the provided pk (primary key) from the URL.
    If the request method is POST, deletes the order from the database.
    Redirects to the home page after successful deletion.

    Parameters:
    - request: The HTTP request object.
    - pk: The primary key of the order to be deleted.

    Returns:
    - Redirects to the home page after successful deletion.
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("/")

    context = {"order": order, "page_title": "Delete Order"}
    return render(request, "accounts/delete_order.html", context)


####USERS#####
# USER LIST
@login_required(login_url="login")
def userListPage(request):
    """
    View function for displaying a list of users.

    Retrieves all users ordered by their date of joining.
    Applies filtering based on the request GET parameters using the UserFilter class.
    Renders the 'users.html' template with the filtered user queryset and filter form.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Rendered HTML template displaying the list of users and filter form.
    """
    users = User.objects.order_by("-date_joined")

    myFilter = UserFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {"users": users, "myFilter": myFilter, "page_title": "Users"}

    return render(request, "accounts/users.html", context)


# VIEW USER
@login_required(login_url="login")
def viewUser(request, pk):
    """
    View function for displaying details of a user.

    Retrieves the user object with the given primary key (pk) or returns a 404 page if not found.
    Retrieves the groups associated with the user.
    Renders the 'view_user.html' template with the user details and associated groups.

    Parameters:
    - request: The HTTP request object.
    - pk: The primary key of the user to be viewed.

    Returns:
    - Rendered HTML template displaying the user details and associated groups.
    """
    user = get_object_or_404(User, pk=pk)
    groups = user.groups.all()

    context = {"user": user, "groups": groups, "page_title": "View User"}

    return render(request, "accounts/view_user.html", context)


# CREATE USER
@login_required(login_url="login")
def createUser(request):
    """
    View function for creating a new user.

    Renders the user creation form initially and processes the form submission.
    If the form is submitted via POST and is valid,
    saves the new user and redirects to the user list page.
    If the form is not valid or the request method is GET,
    renders the 'user_form.html' template with the user creation form.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Rendered HTML template displaying the user creation form or redirecting to the user list page.
    """
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/users")

    context = {"form": form, "page_title": "Create User"}

    return render(request, "accounts/user_form.html", context)


# UPDATE USER
@login_required(login_url="login")
def updateUser(request, pk):
    """
    View function for updating an existing user.

    Retrieves the user object with the specified primary key (pk) from the database.
    Renders the user update form initially with the current user data and processes
    the form submission.
    If the form is submitted via POST and is valid, updates the user's information
    and redirects to the user details page.
    If the form is not valid or the request method is GET, renders the
    'update_user_form.html' template with the user update form pre-filled with the
    current user data.

    Parameters:
    - request: The HTTP request object.
    - pk: The primary key of the user to be updated.

    Returns:
    - Rendered HTML template displaying the user update form or redirecting to the
      user details page.
    """
    user = get_object_or_404(User, pk=pk)
    form = UpdateUserForm(instance=user)

    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            selected_roles = form.cleaned_data.get("groups")
            form.save()
            return redirect("view_user", pk=pk)

    context = {"form": form, "page_title": "Update User", "user": user}
    return render(request, "accounts/update_user_form.html", context)


# DELETE USER
@login_required(login_url="login")
def deleteUser(request, pk):
    """
    View function for deleting a user.

    Retrieves the user object with the specified primary key (pk) from the database.
    Checks if the user is a superuser, and if so, displays an error message and
    redirects to the users list page.
    If the request method is POST, deletes the user from the database and redirects
    to the users list page.
    If the request method is GET or the user is not a superuser, renders the
    'delete_user.html' template with the user details.

    Parameters:
    - request: The HTTP request object.
    - pk: The primary key of the user to be deleted.

    Returns:
    - Rendered HTML template displaying the delete user confirmation page or
      redirecting to the users list page.
    """
    user = get_object_or_404(User, pk=pk)

    if user.is_superuser:
        return redirect("users")

    if request.method == "POST":
        user.delete()
        return redirect("users")

    context = {"user": user, "page_title": "Delete User"}
    return render(request, "accounts/delete_user.html", context)


# REPORTS
@login_required(login_url="login")
def reports(request):
    """
    View function for generating reports on orders and users.

    Retrieves all orders and users from the database.
    Calculates various statistics such as the total number of orders created,
    pending orders, urgent orders, normal orders,
    orders requiring attention, completed orders, and total number of users created.
    Renders the 'reports.html' template with the calculated statistics.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - Rendered HTML template displaying the reports page with order and user statistics.
    """
    orders = Order.objects.all()

    orders_created = orders.count()
    orders_pending = orders.exclude(status="Complete").count()
    orders_urgent = orders.filter(priority="Urgent").exclude(status="Complete").count()
    orders_normal = orders.filter(priority="Normal").exclude(status="Complete").count()
    orders_attention_required = orders.filter(status="Attention Required").count()
    orders_completed = orders.filter(status="Complete").count()

    users = User.objects.filter(groups__name="worker").annotate(
        num_orders_assigned=Count("assigned_orders")
    )
    worker_group = Group.objects.get(name="worker")
    manager_group = Group.objects.get(name="manager")

    users_created = users.count()
    num_workers = User.objects.filter(groups__in=[worker_group]).count()
    num_managers = User.objects.filter(groups__in=[manager_group]).count()

    orders_with_comments = Order.objects.annotate(num_comments=Count("comment"))

    context = {
        "orders_created": orders_created,
        "orders_pending": orders_pending,
        "orders_urgent": orders_urgent,
        "orders_normal": orders_normal,
        "orders_attention_required": orders_attention_required,
        "orders_completed": orders_completed,
        "users_created": users_created,
        "num_workers": num_workers,
        "num_managers": num_managers,
        "orders_with_comments": orders_with_comments,
        "users": users,
        "page_title": "Reports",
    }

    return render(request, "accounts/reports.html", context)
