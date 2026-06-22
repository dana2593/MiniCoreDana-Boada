# ============================================================
#  MODELO  (la "M" de MVC)
# ------------------------------------------------------------
#  Define las 3 tablas del problema y cómo se relacionan.
#  El Modelo SOLO sabe de datos y relaciones: no calcula
#  costos ni recibe requests. Esa separación es lo que hace
#  que el patrón se entienda.
# ============================================================
from django.db import models


class Zona(models.Model):
    """Cada zona de entrega tiene una tarifa fija por kg."""
    id_zona = models.AutoField(primary_key=True)
    nombre_zona = models.CharField(max_length=100)              # Norte, Sur, Centro...
    tarifa_por_kg = models.DecimalField(max_digits=10, decimal_places=2)  # USD por kg

    class Meta:
        db_table = "zonas"

    def __str__(self):
        return f"{self.nombre_zona} (${self.tarifa_por_kg}/kg)"


class Repartidor(models.Model):
    id_repartidor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)            # opcional

    class Meta:
        db_table = "repartidores"

    def __str__(self):
        return self.nombre


class Envio(models.Model):
    id_envio = models.AutoField(primary_key=True)
    repartidor = models.ForeignKey(
        Repartidor, on_delete=models.CASCADE, related_name="envios", db_column="id_repartidor"
    )
    zona = models.ForeignKey(
        Zona, on_delete=models.CASCADE, related_name="envios", db_column="id_zona"
    )
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_envio = models.DateField()

    class Meta:
        db_table = "envios"

    def __str__(self):
        return f"Envío #{self.id_envio} - {self.repartidor.nombre} - {self.fecha_envio}"
