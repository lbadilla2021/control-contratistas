"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

export default function LoginPage() {
  const [email, setEmail] = useState("lbadilla1970@gmail.com");
  const [password, setPassword] = useState("CerroColorado.2020");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"}/auth/login`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        },
      );

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        const detail = (data as { detail?: string } | null)?.detail ?? "No se pudo iniciar sesión";
        throw new Error(detail);
      }

      const data = (await response.json()) as { access_token: string };
      localStorage.setItem("access_token", data.access_token);
      router.push("/dashboard");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Error inesperado";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="mx-auto max-w-md rounded-2xl bg-white p-8 shadow-sm">
      <div className="mb-6 text-center">
        <p className="text-sm uppercase tracking-wide text-primary">Acceso</p>
        <h1 className="text-2xl font-semibold text-slate-900">Inicia sesión</h1>
        <p className="text-sm text-slate-500">Dashboard minimalista para control documental.</p>
      </div>
      <form className="space-y-4" aria-label="Formulario de acceso" onSubmit={handleSubmit}>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-slate-700" htmlFor="email">
            Correo electrónico
          </label>
          <input
            id="email"
            type="email"
            name="email"
            placeholder="admin@empresa.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
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
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm shadow-inner focus:border-primary focus:outline-none"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white transition hover:bg-primary-dark disabled:cursor-not-allowed disabled:opacity-75"
        >
          {loading ? "Ingresando..." : "Entrar"}
        </button>
      </form>
      {error ? <p className="mt-4 text-center text-sm text-red-600">{error}</p> : null}
      <p className="mt-6 text-center text-xs text-slate-500">
        Acceso protegido para administradores, supervisores y contratistas registrados.
      </p>
      <div className="mt-4 text-center text-sm text-primary">
        <Link href="/dashboard">Ir al dashboard</Link>
      </div>
    </section>
  );
}
