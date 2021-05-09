from django.urls import path
from . import views

urlpatterns = [
    # GET routes
    path('', views.loginPage),
    path('registration', views.registration),
    path('dashboard', views.dashboard),
    path('editPage/<int:num>', views.editPage),
    path('delete/<int:num>', views.delete),
    path('logout', views.logout),
    # POST routes
    path('login', views.login),
    path('register', views.register),
    path('createEntry', views.createEntry),
    path('edit/<int:num>', views.edit),
]