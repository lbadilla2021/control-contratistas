# Auditoría técnica

Este informe resume observaciones sobre el estado actual del backend (FastAPI) y el frontend (Next.js) y propone mejoras sin alterar el funcionamiento existente.

## Backend

- **Configuración y secretos**: La configuración usa credenciales y llaves JWT predeterminadas en el código (`CHANGE_ME`, accesos de MinIO y SMTP). Es preferible obtener estos valores de variables de entorno seguras y validar que se definan en producción para evitar despliegues inseguros.【F:backend/app/core/config.py†L4-L27】
- **Autenticación/autorización inexistente**: Los routers exponen operaciones CRUD sin controles de acceso ni dependencias de seguridad, lo que deja la API abierta. Integrar un flujo de login (p. ej., OAuth2 o JWT) y dependencias de `Depends` para roles o permisos reduciría riesgo de uso no autorizado.【F:backend/app/routers/companies.py†L13-L83】【F:backend/app/routers/workers.py†L18-L78】
- **Carga de documentos**: El endpoint acepta archivos pero no valida que la empresa o el trabajador existan, ni limita tamaño o realiza análisis antivirus antes de subirlos a MinIO. Añadir verificaciones previas y límites (content-length, extensión) mejoraría integridad y seguridad de los objetos almacenados.【F:backend/app/routers/documents.py†L25-L74】
- **Notificaciones por email**: El servicio envía correos directamente con SMTP sin manejo granular de errores ni métricas; envolver el envío en lógica de reintentos y registrar fallos facilitaría observabilidad. Además, controlar la frecuencia de alertas por documento evitaría spam en escenarios de reintentos externos.【F:backend/app/services/alert_service.py†L29-L112】
- **Tareas programadas**: La verificación de vencimientos está preparada para ejecutarse periódicamente, pero no hay job scheduler incluido. Integrar algo como Celery/Redis o cronjobs (p. ej., con APScheduler) daría soporte a ejecuciones regulares de `verify_expirations` y `send_document_alerts`.【F:backend/app/services/expiration_service.py†L23-L82】
- **Validación y errores**: Endpoints como creación de trabajadores no validan unicidad de correo ni devuelven códigos específicos para conflictos similares a los de empresa. Añadir reglas de negocio y códigos 409 coherentes evitaría datos duplicados.【F:backend/app/routers/workers.py†L24-L78】
- **Pruebas**: Las pruebas cubren CRUD básico y lógica de expiraciones/alertas usando SQLite en memoria, pero no se ejercitan rutas de documentos ni escenarios de error. Ampliar fixtures para archivos, MinIO mock y SMTP simulado aumentaría confianza en integraciones críticas.【F:backend/tests/test_companies_workers.py†L1-L77】【F:backend/tests/test_expirations.py†L1-L77】【F:backend/tests/test_alerts.py†L1-L87】

## Frontend

- **Login sin lógica**: La página de inicio solo muestra un formulario estático y un enlace al dashboard; falta manejador de envío, validación y retroalimentación de errores. Conectar el submit a una API de autenticación y mostrar estados de carga/errores mejoraría UX y seguridad.【F:frontend/app/page.tsx†L3-L50】
- **Dashboard y API inexistente**: El dashboard intenta consumir `/estadisticas`, endpoint que no existe en el backend actual, lo que genera errores y mensajes genéricos. Conviene alinear las rutas con la API real (empresas, documentos, expiraciones) o exponer un endpoint de métricas antes de consumirlo.【F:frontend/app/dashboard/page.tsx†L10-L85】【F:backend/app/routers/__init__.py†L3-L11】
- **Gestión de token y fetch**: `fetchEstadisticas` usa `getSessionToken` pero construye la URL con variables de entorno opcionales; si faltan, la llamada usa una ruta relativa y puede fallar en SSR. Definir `NEXT_PUBLIC_API_URL` obligatoria y centralizar cabeceras (Authorization, cache) en un cliente evitaría duplicación y errores silenciosos.【F:frontend/app/dashboard/page.tsx†L10-L30】【F:frontend/lib/auth.ts†L1-L12】
- **Estados vacíos y accesibilidad**: Las tarjetas y el texto del dashboard no muestran estados de carga ni skeletons, y los mensajes de error se limitan a una alerta. Incorporar indicadores de carga, descripciones accesibles y manejo de reintentos aumentaría claridad para el usuario.【F:frontend/app/dashboard/page.tsx†L33-L85】

## Recomendaciones transversales

- Documentar un flujo de despliegue local con MinIO/PostgreSQL y variables de entorno requeridas.
- Añadir un pipeline de CI con linting (ruff/black, eslint), pruebas y tipado para evitar regresiones.
- Considerar migrations con Alembic para garantizar consistencia del esquema en entornos distintos de pruebas en memoria.
