from django.urls import path
from .views import user_form_view

urlpatterns = [
    path('', user_form_view, name='user_form'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
]