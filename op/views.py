from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from urllib.parse import quote
from django.http import FileResponse, Http404
from urllib.parse import unquote
import os
import mimetypes
# Create your views here.

@api_view(['GET'])
def ops_pedido(request, pedido):
    
    if not pedido:
        return Response({
            "message": "Error: Se requiere el parametro 'pedido'",
            "data": []
        }) 
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    *,
                    CANTP - PRODUCIDO AS FALTANTE
                FROM (
                    SELECT
                        OP.ID,	
                        OP.OP,
                        LTRIM(RTRIM(OP.NOM)) AS NOM ,
                        RTRIM(OP.COD) AS COD,
                        OP.CANTP,
                        OP.CANTE AS PRODUCIDO,
                        TRIM(DPT.NOM) AS DEPARTAMENTO,
                        OP.ESTADO AS ESTADO,
						TipoMarc + ': ' + Marca AS MARCA
                    FROM [EMP002_INV].[dbo].[OP] OP
                    LEFT JOIN [EMP002_INV].[dbo].[KARDEXA] MOV ON MOV.LOTE = OP.LOTE AND MOV.OP_OC = OP.OP AND OP.COD = MOV.COD
                    INNER JOIN [EMP002_INV].[dbo].[DPTO] DPT ON DPT.COD = OP.CEN
					LEFT JOIN [EMP002_INV].[dbo].[TbFirmasOp] FOP ON FOP.Op = OP.OP
                WHERE OP.LOTE = %s
                GROUP BY 
                    OP.ID, OP.OP, OP.NOM, OP.CANTP, OP.COD, DPT.NOM, OP.CANTE, OP.ESTADO, TipoMarc, Marca
                    ) T
                """,
            [pedido])
            columnas = [col[0] for col in cursor.description]
            datos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
            
            return Response({
                "Message": "Datos obtenidos con exito",
                "data": datos
            })
    except Exception as e:
        return Response({
            "Message": "Error al obtener los datos",
            "Error": str(e)
        }, status=500)

@api_view(['GET'])  
def ficha_tecnica_items_producto(request, codigo):
     
    if not codigo:
        return Response({
            'message': 'Error: Se requiere el parametro del codigo',
            'data': []
        })
     
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    Parte,
                    idParte,
                    P.CodMolde,
                    Cavidades,
                    Ciclo1,
                    LTRIM(RTRIM(M1.Nom)) AS Resina1,
                    LTRIM(RTRIM(M2.Nom)) AS Resinas2, 
                    D.NomProceso AS Decorado, 
                    C.NomMaterial AS Colorante,
                    Alto,
                    P.Ancho,
                    Largo,
                    P.Peso,
                    Diametro,
                    ImgParte
                FROM [EMP002_CTRL].[dbo].[TbFichaProd2] P 
                INNER JOIN [EMP002_INV].[dbo].[Maestro] M1 ON P.Resina1 = M1.Cod 
                LEFT JOIN [EMP002_INV].[dbo].[Maestro] M2 ON P.Resina2 = M2.Cod 
                INNER JOIN [EMP002_CTRL].[dbo].[TbProcesos] D ON P.Decorado = D.IdProceso 
                INNER JOIN [EMP002_CTRL].[dbo].[TbMateriales] C ON P.Colorante = C.IdMaterial
                WHERE P.Codigo = RTRIM(%s)
                    AND Version = (SELECT MAX(Version) FROM [EMP002_CTRL].[dbo].[TbFichaProd2]
                        WHERE Codigo = RTRIM(%s)
                    )
            """, [codigo, codigo])

            columnas = [col[0] for col in cursor.description]
            datos = []
            
            for fila in cursor.fetchall():
                item = dict(zip(columnas, fila))
                if item.get("ImgParte"):
                    ruta_completa = item["ImgParte"]
                    ruta_codificada = quote(ruta_completa, safe='')  # codifica todo
                    item["ImgParte"] = f"/api/imagen?ruta={ruta_codificada}"
                datos.append(item)
            return Response({
                "Message": "Datos obtenidos con exito",
                "data": datos
            })

    except Exception as e:
        return Response({
            "Message": "Error al obtener los datos",
            "Error": str(e)
        }, status=500)
    
@api_view(['GET'])
def ficha_tecnica_producto(request, codigo):

    if not codigo:
        return Response({
            'message': "Error: se requiere parametro 'codigo'",
            'data': []
        })
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    RTRIM(M.Nom) AS Prod,
                    Descripcion,
                    UsoAplica,
                    Partes,
                    AltoTotal, 
                    AnchoTotal,
                    LargoTotal,
                    PesoTotal, 
                    DiamTrotal,
                    ImgProd, 
                    E.NomUsuario Elaboro, 
                    ISNULL(V.NomUsuario,'-') Verifico, 
                    ISNULL(A.NomUsuario,'-') Aprobo, 
                    E1.NomMaTerial as Emp1,
                    E2.NomMaTerial as Emp2,
                    e3.NomMaTerial as Emp3,
                    DimEmp1,
                    DimEmp2,
                    DimEmp3,
                    CantEmp1,
                    CantEmp2,
                    CantEmp3, 
                    Fecha FecElab, 
                    FechaVerif,
                    FechaApr, 
                    Capacidad,
                    MAX(F.Version) AS Version
                from [EMP002_CTRL].[dbo].[TbFichaProd1] as F   
                    LEFT JOIN [EMP002_INV].[dbo].[MAESTRO] as M on F.Codigo = M.COD
                    LEFT JOIN [EMP002_CTRL].[dbo].[TbMateriales] as E1 on E1.IdMaterial = F.Empaque1
                    LEFT JOIN [EMP002_CTRL].[dbo].[TbMateriales] as E2 on E2.IdMaterial = F.Empaque2
                    LEFT JOIN [EMP002_CTRL].[dbo].[TbMateriales] as E3 on E3.IdMaterial = F.Empaque3
                    LEFT JOIN [BdUsuarios].[dbo].[TbUsuarios] E on F.Elaboro = E.IdUsuario
                    LEFT JOIN [BdUsuarios].[dbo].[TbUsuarios] V on F.Verifico = V.IdUsuario
                    LEFT JOIN [BdUsuarios].[dbo].[TbUsuarios] A on F.Aprobo = A.IdUsuario 
                where F.Codigo = %s AND Version = (
                        SELECT MAX(Version)
                        FROM [EMP002_CTRL].[dbo].[TbFichaProd1]
                        WHERE Codigo = RTRIM(%s)
                    )
                GROUP BY M.Nom,
                    Descripcion, UsoAplica, Partes, AltoTotal, AnchoTotal, LargoTotal, PesoTotal, DiamTrotal,
                    ImgProd, E.NomUsuario, V.NomUsuario, A.NomUsuario, E1.NomMaTerial, E2.NomMaTerial, e3.NomMaTerial,
                    DimEmp1, DimEmp2, DimEmp3, CantEmp1, CantEmp2, CantEmp3, Fecha, FechaVerif,
                    FechaApr, Capacidad
                """,[codigo, codigo]
            )
            columnas = [col[0] for col in cursor.description]
            fila = cursor.fetchone()
            if fila:
                datos = dict(zip(columnas, fila))
                if datos.get("ImgProd"):
                    ruta_completa = datos["ImgProd"]
                    ruta_codificada = quote(ruta_completa, safe='')  # codifica todo
                    datos["ImgProd"] = f"/api/imagen?ruta={ruta_codificada}"
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

@api_view(['GET'])
def real_vs_planeado(reques, codigo, op):
    params = {
        "codigo":codigo,
        "op": op
    }

    faltantes = [key for key, value in params.items() if not value]
    if faltantes:
        return Response({
            "error": f"Error: se requiere parametro: {', '.join(faltantes)}"
        }, status=400)
    try:

        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT 
                        ISNULL(FOP.maqJa, 'OP Sin Maquina') AS Maquina,    

                        FP2.Ciclo1 AS CicloPlan,
                        CAST((MM.PMIN + MM.PMAX) / 2 AS DECIMAL) AS CicloReal,

                        FP2.Cavidades AS CavidadesPlan,
                        FP2.Cavidades AS CavidadesReal,

                        FP2.Peso1 AS PesoPlan,
                        ISNULL(CAST(AVG(O3.Peso) AS DECIMAL(14,2)), 0) AS PesoReal,

                        CAST(FP2.Peso1 * OP.CANTP AS DECIMAL(14,2)) AS PesoTotalPlan,
                        ISNULL(CAST(AVG(O3.Peso * OP.CANTP) AS DECIMAL(14,2)), 0) AS PesoTotalReal,

                        CAST(OP.CANTP * 2 / 100.0 AS DECIMAL(14,2)) AS PncPlan,
                        ISNULL(KAgg.PncReal, 0) AS PncReal,

                        CAST(CEILING(SUM(OP1.CANT) * 1.0 / OP.CANTP) AS DECIMAL(14,2)) AS UnidadEmpaque

                    FROM [EMP002_CTRL].[dbo].[TbFichaProd3] FP3 

                    LEFT JOIN [EMP002_CTRL].[dbo].[TbFichaProd2] FP2 ON FP2.Codigo = FP3.Codigo AND FP2.IdParte = FP3.IdParte AND FP3.Version = FP2.Version

                    LEFT JOIN [EMP002_MANT].[dbo].[MAESTRO] MM ON MM.COD = FP2.CodMolde

                    LEFT JOIN [EMP002_INV].[dbo].[OP] OP ON OP.COD = FP3.CodParte
                    
                    INNER JOIN [EMP002_INV].[dbo].[TbFirmasOp] FOP ON FOP.Op = OP.OP
                           
                    LEFT JOIN [EMP002_INV].[dbo].[TbProgMaquinas] PROG ON PROG.Op = OP.OP    
                           
                    LEFT JOIN [EMP002_INV].[dbo].[OP1] OP1 ON OP1.Op = OP.Op

                    LEFT JOIN [EMP002_INV].[dbo].[TbCierreOP2] O2 ON O2.OP = OP.OP

                    LEFT JOIN [EMP002_INV].[dbo].[TbCierreOP3] O3 ON O2.IdEnt = O3.IdEnt
                    LEFT JOIN (SELECT OP_OC, COD,SUM(CANT) AS PncReal
                        FROM [EMP002_INV].[dbo].[KARDEXA]
                        WHERE TIPO IN ('354', '355', '357', '358')
                        GROUP BY OP_OC, COD) KAgg ON KAgg.OP_OC = OP.OP AND KAgg.COD = FP3.CodParte
                    WHERE FP3.CodParte = %s
                    AND OP.OP = %s

                    GROUP BY 
                        FOP.maqJa,
                        FP2.Ciclo1, 
                        FP2.Cavidades, 
                        FP2.Peso1, 
                        MM.PMIN, 
                        MM.PMAX, 
                        OP.CANTP,
                        KAgg.PncReal    
            """, [codigo, op])

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
    

def obtener_imagen(request):
    ruta = request.GET.get("ruta")

    if not ruta:
        raise Http404("Ruta no proporcionada")

    # 🔥 decodificar
    ruta = unquote(ruta)

    print("Ruta recibida:", ruta)  # DEBUG

    if not os.path.exists(ruta):
        print("NO EXISTE")
        raise Http404("Imagen no encontrada")

    tipo, _ = mimetypes.guess_type(ruta)

    return FileResponse(
        open(ruta, 'rb'),
        content_type=tipo or 'application/octet-stream'
    )