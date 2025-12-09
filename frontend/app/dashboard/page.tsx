import Link from "next/link";

export default function DashboardPage() {
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
          <p className="text-3xl font-semibold text-slate-900">0</p>
        </div>
        <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50 p-4 text-center">
          <p className="text-xs uppercase tracking-wide text-slate-500">Por vencer</p>
          <p className="text-3xl font-semibold text-slate-900">0</p>
        </div>
        <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50 p-4 text-center">
          <p className="text-xs uppercase tracking-wide text-slate-500">Vencidos</p>
          <p className="text-3xl font-semibold text-slate-900">0</p>
        </div>
      </div>
      <div className="rounded-xl border border-slate-200 p-4">
        <p className="text-sm font-medium text-slate-700">Tablero pendiente de datos</p>
        <p className="text-sm text-slate-500">
          Integra las APIs de FastAPI para mostrar empresas, trabajadores, documentos y alertas.
        </p>
      </div>
    </div>
  );
}
