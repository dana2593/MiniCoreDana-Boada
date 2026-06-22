# ============================================================
#  SEED DATA
# ------------------------------------------------------------
#  Carga datos de ejemplo directamente en la base (sin CRUD).
#  Se corre con:  python manage.py seed_data
#
#  Los datos reproducen el ejemplo del enunciado para el rango
#  01/05/2025 - 31/05/2025:
#     Andrés -> 5 envíos, 32 kg, Norte ($1.50/kg) -> $48.00
#     Camila -> 3 envíos, 18 kg, Sur  ($2.00/kg) -> $36.00
#     Luis   -> sin envíos en mayo               -> No aplica
#  Marta se agrega para demostrar el caso "varias zonas".
# ============================================================
from datetime import date
from django.core.management.base import BaseCommand
from logistica.models import Zona, Repartidor, Envio


class Command(BaseCommand):
    help = "Carga datos de ejemplo (zonas, repartidores y envíos)."

    def handle(self, *args, **options):
        # Limpiar para que el seed sea idempotente
        Envio.objects.all().delete()
        Repartidor.objects.all().delete()
        Zona.objects.all().delete()

        # ---- Zonas ----
        norte = Zona.objects.create(nombre_zona="Norte", tarifa_por_kg="1.50")
        sur = Zona.objects.create(nombre_zona="Sur", tarifa_por_kg="2.00")
        centro = Zona.objects.create(nombre_zona="Centro", tarifa_por_kg="1.00")

        # ---- Repartidores ----
        andres = Repartidor.objects.create(nombre="Andrés", email="andres@logistica.com")
        camila = Repartidor.objects.create(nombre="Camila", email="camila@logistica.com")
        luis = Repartidor.objects.create(nombre="Luis", email="luis@logistica.com")
        marta = Repartidor.objects.create(nombre="Marta", email="marta@logistica.com")

        # ---- Envíos de Andrés: 5 envíos en Norte, total 32 kg -> $48.00 ----
        for peso, dia in [(5, 3), (8, 7), (6, 12), (7, 18), (6, 25)]:  # suma 32 kg
            Envio.objects.create(repartidor=andres, zona=norte, peso_kg=peso,
                                 fecha_envio=date(2025, 5, dia))

        # ---- Envíos de Camila: 3 envíos en Sur, total 18 kg -> $36.00 ----
        for peso, dia in [(6, 5), (5, 14), (7, 22)]:  # suma 18 kg
            Envio.objects.create(repartidor=camila, zona=sur, peso_kg=peso,
                                 fecha_envio=date(2025, 5, dia))

        # ---- Luis: solo tiene envíos FUERA de mayo -> "No aplica" en el rango ----
        Envio.objects.create(repartidor=luis, zona=centro, peso_kg=10,
                             fecha_envio=date(2025, 4, 28))

        # ---- Marta: envíos en VARIAS zonas dentro de mayo (demuestra la nota) ----
        # 4 kg * 1.50 (Norte) + 5 kg * 2.00 (Sur) = 6.00 + 10.00 = 16.00
        Envio.objects.create(repartidor=marta, zona=norte, peso_kg=4,
                             fecha_envio=date(2025, 5, 10))
        Envio.objects.create(repartidor=marta, zona=sur, peso_kg=5,
                             fecha_envio=date(2025, 5, 20))

        self.stdout.write(self.style.SUCCESS(
            "Datos de ejemplo cargados correctamente."
        ))
