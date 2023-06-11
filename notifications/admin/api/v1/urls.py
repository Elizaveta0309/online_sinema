
from django.urls import path

from api.v1 import views

urlpatterns = [
    path('templates/', views.get_template_by_param),
    path('templates/<uuid:template_id>/', views.get_template_by_id),
    path('configs/<str:config_name>/', views.get_config_value),
]
