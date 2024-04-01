from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),

    path("", views.home, name="home"),
    path("view_order/<str:pk>/", views.viewOrder, name="view_order"),
    path("create_order/", views.createOrder, name="create_order"),
    path("<str:pk>/comment", views.addComment, name="add_comment"),
    path('delete_comment/<str:comment_id>/', views.deleteComment, name='delete_comment'),
    path("update_order/<str:pk>/", views.updateOrder, name="update_order"),
    path("delete_order/<str:pk>/", views.deleteOrder, name="delete_order"),

    path("users/", views.userListPage, name="users"),
    path("view_user/<str:pk>/", views.viewUser, name="view_user"),
    path("create_user/", views.createUser, name="create_user"),
    path("update_user/<str:pk>/", views.updateUser, name="update_user"),
    path("delete_user/<str:pk>/", views.deleteUser, name="delete_user"),     
]