import Link from "next/link";

export default function LoginPage() {
  return (
    <section className="mx-auto max-w-md rounded-2xl bg-white p-8 shadow-sm">
      <div className="mb-6 text-center">
        <p className="text-sm uppercase tracking-wide text-primary">Acceso</p>
        <h1 className="text-2xl font-semibold text-slate-900">Inicia sesión</h1>
        <p className="text-sm text-slate-500">Dashboard minimalista para control documental.</p>
      </div>
      <form className="space-y-4" aria-label="Formulario de acceso">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-slate-700" htmlFor="email">
            Correo electrónico
          </label>
          <input
            id="email"
            type="email"
            name="email"
            placeholder="admin@empresa.com"
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-inner focus:border-primary focus:outline-none"
          />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-slate-700" htmlFor="password">
            Contraseña
          </label>
          <input
            id="password"
            type="password"
            name="password"
            placeholder="********"
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-inner focus:border-primary focus:outline-none"
          />
        </div>
        <button
          type="submit"
          className="w-full rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white transition hover:bg-primary-dark"
        >
          Entrar
        </button>
      </form>
      <p className="mt-6 text-center text-xs text-slate-500">
        Acceso protegido para administradores, supervisores y contratistas registrados.
      </p>
      <div className="mt-4 text-center text-sm text-primary">
        <Link href="/dashboard">Ir al dashboard</Link>
      </div>
    </section>
  );
}
