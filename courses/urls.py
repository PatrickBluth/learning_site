
from django.urls import path


from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_pk>/<int:step_pk>/', views.text_detail, name='text'),
    path('<int:course_pk>/<int:step_pk>/', views.quiz_detail, name='quiz'),
    path('<int:pk>/', views.course_detail, name='detail'),
]