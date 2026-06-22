from django.urls import path
from . import views

urlpatterns = [
    path("costos/", views.costos_por_repartidor, name="costos_por_repartidor"),
]
