from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.event_create, name='event_create'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/attendance/', views.event_attendance, name='event_attendance'),

    # Universities
    path('universities/', views.university_map, name='university_map'),
    path('universities/add/', views.university_create, name='university_create'),
    path('universities/<int:pk>/edit/', views.university_edit, name='university_edit'),
    path('universities/<int:pk>/delete/', views.university_delete, name='university_delete'),

    # Reports
    path('reports/', views.reports_index, name='reports_index'),
    path('reports/download/', views.report_pdf, name='report_pdf'),

    # API
    path('api/stats/', views.api_dashboard_stats, name='api_stats'),
]
