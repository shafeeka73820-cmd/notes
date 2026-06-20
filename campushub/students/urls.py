from django.urls import path
from . import views
from .cbv_views import (
    StudentListView, StudentDetailView,
    StudentCreateView, StudentUpdateView, StudentDeleteView,
    DashboardView
)

app_name = 'students'

urlpatterns = [
    path('', StudentListView.as_view(), name='index'),
    path('<int:roll>/', StudentDetailView.as_view(), name='detail'),
    path('departments/', views.departments, name='departments'),
    path('departments/<str:code>/', views.department_detail, name='department_detail'),
    path('about/', views.about, name='about'),
    path('stats/', views.stats, name='stats'),
    path('placements/', views.placements, name='placements'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('feedback/', views.feedback, name='feedback'),
    path('add/', StudentCreateView.as_view(), name='add'),
    path('<int:roll>/edit/', StudentUpdateView.as_view(), name='edit'),
    path('<int:roll>/delete/', StudentDeleteView.as_view(), name='delete'),
    path('register/', views.register, name='register'),
    path('portal/', views.portal, name='portal'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('documents/<int:pk>/delete/', views.delete_document, name='delete_document'),
]
