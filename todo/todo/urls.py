
from django.contrib import admin
from django.urls import path
from .views import*

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',sign,name='sign' ),
    path('login/', user_login,name='login'),
    path('todo/', todo,name='todo'),
    path('edit/<int:id>', edit,name='edit'),
    path('delete/<int:id>', delete,name='delete'),
    path('signout/', signout,name='signout'),



]
