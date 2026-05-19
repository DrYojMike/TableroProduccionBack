from django.urls import path
from .views import(ops_pedido, 
                ficha_tecnica_items_producto, 
                ficha_tecnica_producto, 
                real_vs_planeado,
                obtener_imagen)
urlpatterns = [
    path('list/<str:pedido>/', ops_pedido),
    path('ficha/tecnica/items/<str:codigo>/', ficha_tecnica_items_producto),
    path('ficha/tecnica/producto/<str:codigo>/', ficha_tecnica_producto),
    path('planeado/vs/real/<str:codigo>/<int:op>/', real_vs_planeado),
    path('api/imagen', obtener_imagen),
]

