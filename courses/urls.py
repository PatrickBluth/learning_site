
from django.urls import path


from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_pk>/t<int:step_pk>/', views.text_detail, name='text'),
    path('<int:course_pk>/q<int:step_pk>/', views.quiz_detail, name='quiz'),
    path('<int:course_pk>/create_quiz/', views.quiz_create, name='quiz_create'),
    path('<int:course_pk>/edit_quiz/<int:quiz_pk>/', views.quiz_edit, name='quiz_edit'),
    path('<int:pk>/', views.course_detail, name='detail'),
]