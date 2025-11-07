from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.application_list, name='application_list'),
    path('add/', views.application_add, name='application_add'),
    path('edit/<int:pk>/', views.application_edit, name='application_edit'),
    path('delete/<int:pk>/', views.application_delete, name='application_delete'),

    # tracker/urls.py (append these paths)
    path('dsa/', views.problem_list, name='problem_list'),
    path('dsa/add/', views.problem_create, name='problem_create'),
    path('dsa/edit/<int:pk>/', views.problem_update, name='problem_update'),
    path('dsa/delete/<int:pk>/', views.problem_delete, name='problem_delete'),

    # Aptitude Tracker
    path('aptitude/', views.aptitude_list, name='aptitude_list'),
    path('aptitude/add/', views.aptitude_create, name='aptitude_create'),
    path('aptitude/<int:pk>/edit/', views.aptitude_update, name='aptitude_update'),
    path('aptitude/<int:pk>/delete/', views.aptitude_delete, name='aptitude_delete'),

   # -------------------- Placement Analytics --------------------
    path('analytics/placement/status/', views.placement_status_distribution, name='placement_status'),
    path('analytics/placement/company/', views.placement_applications_per_company, name='placement_company'),

    # -------------------- DSA Analytics --------------------
    path('analytics/dsa/topic/', views.dsa_progress_per_topic, name='dsa_topic'),
    path('analytics/dsa/time/', views.dsa_progress_over_time, name='dsa_time'),

    # -------------------- Aptitude Analytics --------------------
    path('analytics/aptitude/topic/', views.aptitude_average_per_topic, name='aptitude_topic'),  # corrected
    path('analytics/aptitude/time/', views.aptitude_scores_over_time, name='aptitude_time'),

    # Dashboard page
    path('analytics/dashboard/', views.analytics_dashboard, name='analytics_dashboard'),

    # tracker/urls.py
    path('resume-analyzer/', views.resume_analyzer, name='resume_analyzer'),


    # Mock Interview Bot
    path("start/", views.start_interview, name="start_interview"),
    path("answer/", views.submit_answer, name="submit_answer"),
    path("mock-interview/", views.mock_interview_view, name="mock_interview"),  # <- important

    # # Login / Logout
    # path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    path('admin/', admin.site.urls),
    


]



