from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
# Create your views here.

@api_view(['GET'])
def obtener_pedidos_cliente(request):
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        offset = (page - 1) * limit

        estado = request.GET.get('estado')
        vendedor = request.GET.get('vendedor')
        busqueda = request.GET.get('q')

        query = """
            SELECT
                NUM,
                NOM,
                ESTADO,
                ISNULL(AG.Agente, 'SIN AGENTE') AS VENDEDOR
            FROM [EMP002_FACT].[dbo].[PEDIDOS] P
            LEFT JOIN [Diseño].[dbo].[Agentes] AG 
                ON AG.IdAgente = P.VENDEDOR
            WHERE 1=1
        """

        params = []

        if estado:
            query += " AND ESTADO = %s"
            params.append(estado)

        if vendedor:
            query += " AND AG.Agente LIKE %s"
            params.append(f"%{vendedor}%")

        if busqueda:
            query += """
                AND (
                    NUM LIKE %s OR 
                    NOM LIKE %s
                )
            """
            params.extend([f"%{busqueda}%", f"%{busqueda}%"])

        # 🔥 paginación
        query += " ORDER BY P.FECHA OFFSET %s ROWS FETCH NEXT %s ROWS ONLY"
        params.extend([offset, limit])

        with connection.cursor() as cursor:
            cursor.execute(query, params)

            columnas = [col[0] for col in cursor.description]
            datos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

        return Response({
            "page": page,
            "limit": limit,
            "data": datos
        })

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=500)
    
@api_view(['GET'])
def encabezado_proyecto(request, pedido):
    if not pedido:
        return Response({
            "Message": "Error: Se requiere el parámetro 'pedido'",
            "data": []
        }, status=400)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    TRIM(P.NOM) AS NOM,
                    TRIM(ISNULL(C.NOM, 'N/A')) AS Cliente,
                    TRIM(P.NUM) AS NUM,
                    P.CANT,
                    P.cant - SUM(CASE 
                        WHEN k.TIPO IN ('353') 
                            THEN k.CANT
                        ELSE 0 
                    END) AS FALTANTE,
                    P.FECHA AS INICIO,
                    P.ENTREGA AS FINAL,
                    TRIM(P.COD) AS COD,
                    P.ESTADO AS ESTADO 
                FROM [EMP002_FACT].[dbo].[PEDIDOS] P
                LEFT JOIN [EMP002_INV].[dbo].[KARDEXA] k ON k.LOTE = p.num
                LEFT JOIN [EMP002_FACT].[dbo].[CLIENTES] C ON C.COD = P.CLIENTE 
                WHERE P.NUM = %s
                GROUP BY P.NOM,
                    C.NOM,
                    P.NUM,
                    P.cant,P.FECHA,
                    P.ENTREGA,
                    P.COD,
                    P.ESTADO
                """, [pedido])
            

            columnas = [col[0] for col in cursor.description]
            fila = cursor.fetchone()
            if fila:
                datos = dict(zip(columnas, fila))
            else:
                datos = {}
            
            return Response({
                "Message": "Datos obtenidos con exito",
                "data": datos
            })
    except Exception as e:
        return Response({
            "Message": "Error al obtener los datos",
            "Error": str(e)
        }, status=500)