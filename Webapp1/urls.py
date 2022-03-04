"""Webapp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from myapp import views
# from myapp.views import GetAllEmployeeAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pagination',views.welcome),
    path('form',views.form),
    # path('',include('myapp.urls')),
    # path('show', views.show),
    # path('coures',views.EmployeeSerializer.as_view()),
    # path('employee',GetAllEmployeeAPIView.as_view()),
    path('api/', include('myapp.urls')),
    # path('search_elas/',views.search_elas),
    path('',views.pagination),
    path('data',views.form),
    path('search', views.search),
    path('search1', views.search1),
    # path('edit/<int:Id>', views.edit),
    # path('update/<int:Id>', views.update),
    path('export-excel', views.export_excel, name='export_excel'),
    path('export-csv', views.export_csv, name='export_csv'),]
