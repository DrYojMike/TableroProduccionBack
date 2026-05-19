from .views import obtener_pedidos_cliente, encabezado_proyecto
from django.urls import path
urlpatterns = [
    path('list/', obtener_pedidos_cliente),
    path('encabezado/<str:pedido>/', encabezado_proyecto)
]
