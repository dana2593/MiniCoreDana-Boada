# ============================================================
#  LÓGICA DE NEGOCIO  (apoya al Controlador)
# ------------------------------------------------------------
#  Aquí vive el "Mini Core": el cálculo del costo por
#  repartidor en un rango de fechas.
#
#  Lo separamos del Controlador (views.py) a propósito:
#    - El Controlador se encarga de recibir el request y responder.
#    - Esta función se encarga SOLO de la regla de negocio.
#  Así el cálculo se puede explicar, probar y reutilizar solo.
# ============================================================
from collections import defaultdict
from decimal import Decimal

from .models import Repartidor, Envio


def calcular_costos(fecha_inicio, fecha_fin):
    """
    Para cada repartidor:
      1. Filtra sus envíos cuya fecha_envio esté en [fecha_inicio, fecha_fin].
      2. Por cada envío: peso_kg * tarifa_por_kg de SU zona.
      3. Costo total = suma de todos esos productos.

    Si un repartidor tiene envíos en varias zonas, el cálculo es por
    envío y luego se suma (tal como pide la nota del enunciado).

    Devuelve una lista de dicts lista para mostrar en la tabla.
    """
    # Traemos los envíos del rango. select_related evita consultas extra
    # al acceder a .repartidor y .zona (más eficiente y más claro).
    envios = (
        Envio.objects
        .filter(fecha_envio__range=(fecha_inicio, fecha_fin))
        .select_related("repartidor", "zona")
    )

    # Acumuladores por repartidor
    acumulado = defaultdict(lambda: {
        "cantidad_envios": 0,
        "total_kg": Decimal("0"),
        "costo_total": Decimal("0"),
        "zonas": {},  # nombre_zona -> tarifa (para mostrar la columna Zona/Tarifa)
    })

    for envio in envios:
        rep_id = envio.repartidor_id
        costo_envio = envio.peso_kg * envio.zona.tarifa_por_kg  # peso × tarifa

        acumulado[rep_id]["cantidad_envios"] += 1
        acumulado[rep_id]["total_kg"] += envio.peso_kg
        acumulado[rep_id]["costo_total"] += costo_envio
        acumulado[rep_id]["zonas"][envio.zona.nombre_zona] = envio.zona.tarifa_por_kg

    # Construimos la respuesta para TODOS los repartidores.
    # Los que no tienen envíos en el período salen con costo 0 / "No aplica"
    # (igual que el repartidor "Luis" del ejemplo del enunciado).
    resultado = []
    for rep in Repartidor.objects.all().order_by("nombre"):
        datos = acumulado.get(rep.id_repartidor)

        if not datos or datos["cantidad_envios"] == 0:
            resultado.append({
                "id_repartidor": rep.id_repartidor,
                "nombre": rep.nombre,
                "cantidad_envios": 0,
                "total_kg": 0.0,
                "zona": "—",
                "tarifa_por_kg": None,
                "costo_total": 0.0,
                "aplica": False,  # el front muestra "No aplica"
            })
            continue

        # Columna Zona / Tarifa: una sola zona -> se muestra directa;
        # varias zonas -> "Varias zonas".
        zonas = datos["zonas"]
        if len(zonas) == 1:
            (nombre_zona, tarifa), = zonas.items()
            zona_display = nombre_zona
            tarifa_display = float(tarifa)
        else:
            zona_display = "Varias zonas"
            tarifa_display = None

        resultado.append({
            "id_repartidor": rep.id_repartidor,
            "nombre": rep.nombre,
            "cantidad_envios": datos["cantidad_envios"],
            "total_kg": float(datos["total_kg"]),
            "zona": zona_display,
            "tarifa_por_kg": tarifa_display,
            "costo_total": round(float(datos["costo_total"]), 2),
            "aplica": True,
        })

    return resultado
