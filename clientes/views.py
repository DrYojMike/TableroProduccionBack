from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
# Create your views here.

@api_view(['GET'])
def obtener_clientes(request):
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT 
                       ID,
                       LTRIM(RTRIM(NOM)) AS Name,
                       LTRIM(RTRIM(NIT)) AS Nit
                FROM [EMP002_FACT].[dbo].[CLIENTES]
                """
                       #[cliente]
            )
        columnas = [col[0] for col in cursor.description]
        datos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        return Response({"Message": "Datos obtenidos con exito",
                         'data': datos})  