// La URL del backend se parametriza por variable de entorno.
// En local apunta a http://localhost:8000; en producción se define
// VITE_API_URL en el hosting (Render/Vercel/etc.).
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function obtenerCostos(fechaInicio, fechaFin) {
  const url = `${API_URL}/api/costos/?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
  const resp = await fetch(url);
  const data = await resp.json();
  if (!resp.ok) {
    throw new Error(data.error || "Error al consultar el backend.");
  }
  return data;
}
