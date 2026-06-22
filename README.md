# Mini Core — Costos de Envío por Repartidor (MVC con Django + React)

Aplicación funcional que calcula el **costo total de envíos por repartidor** dentro de un rango de fechas, aplicando la **tarifa por kilogramo según la zona** de entrega.

El objetivo del proyecto es **demostrar el patrón MVC** ante un problema concreto de logística.

---

## MVC utilizado

Este proyecto separa responsabilidades siguiendo el patrón **MVC**, repartido entre Django (backend) y React (frontend):

| Capa MVC | Dónde está | Qué hace |
|---|---|---|
| **Modelo** | `backend/logistica/models.py` | Define las 3 tablas (`Repartidor`, `Zona`, `Envio`) y sus relaciones. Solo datos. |
| **Controlador** | `backend/logistica/views.py` + `services.py` | Recibe el rango de fechas, valida, ejecuta la regla de negocio (peso × tarifa) y devuelve JSON. |
| **Vista** | `frontend/src/App.jsx` | Formulario de fechas y tabla de resultados. Solo presentación; pide los datos al Controlador. |

> Nota sobre terminología: Django usa el patrón **MTV** (Model–Template–View). Lo que Django llama "view" (`views.py`) cumple el rol del **Controlador** en MVC, y la **Vista** real de cara al usuario es React. Por eso el `services.py` separa la lógica de negocio del manejo del request.

---

## Descripción breve

- Una sola pantalla principal: formulario con **Fecha Inicio** y **Fecha Fin**.
- Al consultar, el backend filtra los envíos en el rango y, por cada envío, calcula `peso_kg × tarifa_por_kg` de su zona.
- El costo total por repartidor es la suma de todos sus envíos en el período (si tiene envíos en varias zonas, se calcula por envío y se suman).
- Los repartidores sin envíos en el rango se muestran como **"No aplica" / $0.00**.

---

## Estructura del proyecto

```
mini-core-logistica/
├── backend/                  # Django (Modelo + Controlador)
│   ├── config/               # settings, urls, wsgi
│   └── logistica/
│       ├── models.py         # MODELO
│       ├── services.py       # lógica de negocio (el cálculo)
│       ├── views.py          # CONTROLADOR (endpoint /api/costos/)
│       └── management/commands/seed_data.py   # datos de ejemplo
└── frontend/                 # React + Vite (Vista)
    └── src/
        ├── App.jsx           # VISTA principal
        └── api.js            # llamada al backend
```

---

## Cómo correrlo localmente

### 1. Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data      # carga zonas, repartidores y envíos de ejemplo
python manage.py runserver      # queda en http://localhost:8000
```

Endpoint: `http://localhost:8000/api/costos/?fecha_inicio=2025-05-01&fecha_fin=2025-05-31`

### 2. Frontend (React + Vite)

En otra terminal:

```bash
cd frontend
npm install
cp .env.example .env            # VITE_API_URL=http://localhost:8000
npm run dev                     # queda en http://localhost:5173
```

Abre **http://localhost:5173** y prueba el rango `2025-05-01` a `2025-05-31`.

---

## Resultado esperado (rango 01/05/2025 – 31/05/2025)

| Repartidor | Envíos | Total kg | Zona | Tarifa/kg | Costo Total |
|---|---|---|---|---|---|
| Andrés | 5 | 32 kg | Norte | $1.50 | **$48.00** |
| Camila | 3 | 18 kg | Sur | $2.00 | **$36.00** |
| Luis | 0 | — | — | — | No aplica |
| Marta | 2 | 9 kg | Varias zonas | — | **$16.00** |

(Marta demuestra el caso de varias zonas: 4 kg × $1.50 + 5 kg × $2.00 = $16.00.)

---

## Video explicativo

🎥 **Link al video:** _(pega aquí tu link de Loom o YouTube)_

---

## Info base del MVC investigado

- Documentación oficial Django: https://docs.djangoproject.com/
- Documentación Django REST Framework: https://www.django-rest-framework.org/
- Documentación React: https://react.dev/
- Video de referencia 1: _(pega aquí)_
- Video de referencia 2: _(pega aquí)_

---

## Contacto

- Correo institucional UDLA: _alumno.apellido@udla.edu.ec_
- Correo alternativo: _(opcional)_
