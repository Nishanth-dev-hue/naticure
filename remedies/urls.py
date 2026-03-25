from django.urls import path
from . import views

urlpatterns = [
    # Template routes
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('remedies/', views.search_remedy, name='search_remedy'),
    path('suggest/', views.suggest_remedy, name='suggest_remedy'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/remedies/', views.admin_manage_remedies, name='admin_manage_remedies'),
    path('admin-panel/suggestions/', views.admin_review_suggestions, name='admin_review_suggestions'),
    path('admin-panel/feedback/', views.admin_view_feedback, name='admin_view_feedback'),
    path('admin-panel/unknown-symptoms/', views.admin_unknown_symptoms, name='admin_unknown_symptoms'),

    # API routes
    path('api/remedies/', views.api_get_remedies, name='api_get_remedies'),
    path('api/suggest-remedy/', views.api_suggest_remedy, name='api_suggest_remedy'),
    path('api/feedback/', views.api_feedback, name='api_feedback'),
    path('api/unknown-symptom/', views.api_unknown_symptom, name='api_unknown_symptom'),
    
    path('api/admin/remedies/', views.api_admin_get_remedies, name='api_admin_get_remedies'),
    path('api/admin/remedies/create/', views.api_admin_remedy_create, name='api_admin_remedy_create'),
    path('api/admin/remedies/update/<int:pk>/', views.api_admin_remedy_update, name='api_admin_remedy_update'),
    path('api/admin/remedies/delete/<int:pk>/', views.api_admin_remedy_delete, name='api_admin_remedy_delete'),
    
    path('api/admin/suggestions/', views.api_admin_get_suggestions, name='api_admin_get_suggestions'),
    path('api/admin/approve/<int:pk>/', views.api_admin_approve_suggestion, name='api_admin_approve_suggestion'),
    path('api/admin/reject/<int:pk>/', views.api_admin_reject_suggestion, name='api_admin_reject_suggestion'),

    path('api/admin/feedback/', views.api_admin_get_feedback, name='api_admin_get_feedback'),
    path('api/admin/unknown-symptoms/', views.api_admin_get_unknown_symptoms, name='api_admin_get_unknown_symptoms'),
    path('manifest.json', views.manifest, name='manifest'),
    path('service-worker.js', views.service_worker, name='service_worker'),
]
