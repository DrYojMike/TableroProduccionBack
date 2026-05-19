from django.urls import path
from .views import obtener_clientes

urlpatterns = [
    path('list/', obtener_clientes),
]
