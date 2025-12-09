import Link from "next/link";
import { getSessionToken } from "@/lib/auth";

interface Estadisticas {
  vigentes: number;
  porVencer: number;
  vencidos: number;
}

async function fetchEstadisticas(): Promise<Estadisticas> {
  const token = getSessionToken();
  const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? process.env.API_URL ?? "";
  const url = `${baseUrl}/estadisticas`;

  const response = await fetch(url, {
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error("No se pudo obtener la información de estadísticas");
  }

  const data = await response.json();

  return {
    vigentes: Number(data.vigentes ?? 0),
    porVencer: Number(data.por_vencer ?? 0),
    vencidos: Number(data.vencidos ?? 0)
  };
}

export default async function DashboardPage() {
  let estadisticas: Estadisticas = { vigentes: 0, porVencer: 0, vencidos: 0 };
  let errorMessage = "";

  try {
    estadisticas = await fetchEstadisticas();
  } catch (error) {
    console.error(error);
    errorMessage = "No se pudieron cargar las estadísticas.";
  }

  return (
    <div className="space-y-6 rounded-2xl bg-white p-8 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-wide text-primary">Dashboard</p>
          <h1 className="text-2xl font-semibold text-slate-900">ControlDoc</h1>
          <p className="text-sm text-slate-500">Resumen de documentos y vencimientos.</p>
        </div>
        <Link
          href="/"
          className="text-sm font-medium text-primary underline-offset-2 hover:underline"
        >
          Salir
        </Link>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50 p-4 text-center">
          <p className="text-xs uppercase tracking-wide text-slate-500">Vigentes</p>
          <p className="text-3xl font-semibold text-slate-900">{estadisticas.vigentes}</p>
        </div>
        <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50 p-4 text-center">
          <p className="text-xs uppercase tracking-wide text-slate-500">Por vencer</p>
          <p className="text-3xl font-semibold text-slate-900">{estadisticas.porVencer}</p>
        </div>
        <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50 p-4 text-center">
          <p className="text-xs uppercase tracking-wide text-slate-500">Vencidos</p>
          <p className="text-3xl font-semibold text-slate-900">{estadisticas.vencidos}</p>
        </div>
      </div>
      <div className="rounded-xl border border-slate-200 p-4">
        <p className="text-sm font-medium text-slate-700">Tablero pendiente de datos</p>
        <p className="text-sm text-slate-500">
          Integra las APIs de FastAPI para mostrar empresas, trabajadores, documentos y alertas.
        </p>
        {errorMessage && (
          <p className="mt-2 text-sm text-amber-600" role="alert">
            {errorMessage}
          </p>
        )}
      </div>
    </div>
  );
}
