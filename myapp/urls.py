from django.urls import path

from . import views

urlpatterns = [
    # path('employees', views.ListCreateEmployeeView.as_view()),
    # path('employees/<int:Id>', views.UpdateDeleteEmployeeView.as_view()),
    # path('employee',views.employeeApi),
    # path('employee/<int:id>',views.employeeApi),
    
    path('tutorials', views.tutorial_list),
    path('tutorials/<int:pk>', views.tutorial_detail),
    path('tutorials/published', views.tutorial_list_published)
]