# ============================================================
#  CONTROLADOR  (la "C" de MVC)
# ------------------------------------------------------------
#  OJO con la terminología: Django llama "views" a esto, pero
#  en el patrón MVC clásico esto es el CONTROLADOR.
#  Su trabajo:
#    1. Recibir el request (el rango de fechas).
#    2. Validar la entrada.
#    3. Pedirle el cálculo a la lógica de negocio (services.py).
#    4. Devolver la respuesta (JSON) que consumirá la Vista (React).
#  No tiene reglas de negocio dentro: solo orquesta.
# ============================================================
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services import calcular_costos


def _parse_fecha(valor):
    """Convierte 'YYYY-MM-DD' a date. Devuelve None si es inválida."""
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


@api_view(["GET"])
def costos_por_repartidor(request):
    """
    GET /api/costos/?fecha_inicio=2025-05-01&fecha_fin=2025-05-31
    """
    fecha_inicio = _parse_fecha(request.query_params.get("fecha_inicio"))
    fecha_fin = _parse_fecha(request.query_params.get("fecha_fin"))

    if not fecha_inicio or not fecha_fin:
        return Response(
            {"error": "Debes enviar fecha_inicio y fecha_fin en formato YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if fecha_inicio > fecha_fin:
        return Response(
            {"error": "fecha_inicio no puede ser mayor que fecha_fin."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    datos = calcular_costos(fecha_inicio, fecha_fin)
    return Response({
        "rango": {"fecha_inicio": str(fecha_inicio), "fecha_fin": str(fecha_fin)},
        "resultados": datos,
    })
