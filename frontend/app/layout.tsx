import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ControlDoc",
  description: "Dashboard de control documental para contratistas"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className="min-h-screen bg-slate-50 text-slate-900">
        <div className="mx-auto flex min-h-screen max-w-5xl flex-col px-4 py-8">
          <header className="mb-8 flex items-center justify-between">
            <div className="flex items-center gap-2 text-lg font-semibold text-primary">
              <span className="h-3 w-3 rounded-full bg-primary" aria-hidden />
              ControlDoc
            </div>
            <nav className="text-sm text-slate-500">SaaS Control Documental</nav>
          </header>
          <main className="flex-1">{children}</main>
          <footer className="mt-8 text-center text-xs text-slate-400">
            Construido con Next.js · FastAPI · PostgreSQL · MinIO
          </footer>
        </div>
      </body>
    </html>
  );
}
