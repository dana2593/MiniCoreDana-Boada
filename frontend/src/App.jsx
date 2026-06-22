// ============================================================
//  VISTA  (la "V" de MVC)
// ------------------------------------------------------------
//  React es la capa de presentación: el formulario de fechas
//  y la tabla de resultados. NO calcula costos; solo pide los
//  datos al Controlador (backend) y los muestra.
// ============================================================
import { useState } from "react";
import { obtenerCostos } from "./api";

function formatoUSD(valor) {
  return `$${Number(valor).toFixed(2)}`;
}

export default function App() {
  const [fechaInicio, setFechaInicio] = useState("2025-05-01");
  const [fechaFin, setFechaFin] = useState("2025-05-31");
  const [resultados, setResultados] = useState([]);
  const [rango, setRango] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  async function consultar(e) {
    e.preventDefault();
    setError("");
    setCargando(true);
    try {
      const data = await obtenerCostos(fechaInicio, fechaFin);
      setResultados(data.resultados);
      setRango(data.rango);
    } catch (err) {
      setError(err.message);
      setResultados([]);
      setRango(null);
    } finally {
      setCargando(false);
    }
  }

  return (
    <div className="contenedor">
      <header>
        <h1>Costos de Envío por Repartidor</h1>
        <p className="subtitulo">
          Filtra por rango de fechas y calcula el costo total de envíos
          (peso × tarifa por zona).
        </p>
      </header>

      <form className="filtro" onSubmit={consultar}>
        <div className="campo">
          <label htmlFor="inicio">Fecha Inicio</label>
          <input
            id="inicio"
            type="date"
            value={fechaInicio}
            onChange={(e) => setFechaInicio(e.target.value)}
          />
        </div>
        <div className="campo">
          <label htmlFor="fin">Fecha Fin</label>
          <input
            id="fin"
            type="date"
            value={fechaFin}
            onChange={(e) => setFechaFin(e.target.value)}
          />
        </div>
        <button type="submit" disabled={cargando}>
          {cargando ? "Calculando..." : "Calcular"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {rango && (
        <p className="rango">
          Rango: {rango.fecha_inicio} — {rango.fecha_fin}
        </p>
      )}

      {resultados.length > 0 && (
        <table className="tabla">
          <thead>
            <tr>
              <th>Repartidor</th>
              <th>Envíos</th>
              <th>Total kg</th>
              <th>Zona</th>
              <th>Tarifa/kg</th>
              <th>Costo Total</th>
            </tr>
          </thead>
          <tbody>
            {resultados.map((r) => (
              <tr key={r.id_repartidor} className={r.aplica ? "" : "sin-envios"}>
                <td>{r.nombre}</td>
                <td>{r.aplica ? r.cantidad_envios : 0}</td>
                <td>{r.aplica ? `${r.total_kg} kg` : "—"}</td>
                <td>{r.zona}</td>
                <td>{r.tarifa_por_kg != null ? formatoUSD(r.tarifa_por_kg) : "—"}</td>
                <td>{r.aplica ? formatoUSD(r.costo_total) : "No aplica"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
