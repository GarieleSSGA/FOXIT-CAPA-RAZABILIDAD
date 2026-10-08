# Capa de Trazabilidad Documental — Foxit

Capa de trazabilidad para el expediente penal peruano, construida sobre las APIs de Foxit.

**El problema.** El expediente penal se cumple en papel. El papel no tiene dueño, no tiene reloj y no tiene memoria. Cuando un plazo vence, la persona sale libre y nadie responde, porque no hay registro que muestre quién tenía el caso ni a quién se le avisó.

**La respuesta.** Cuatro pilares: sello de integridad por documento, versionado inmutable, registro de transferencias con acuse de recibo, y reloj de plazos. Tres de cuatro funcionan hoy y están verificados. El cuarto —firma con identidad— requiere una cuenta de Foxit eSign que esta cuenta no tiene, y el hueco está declarado con total honestidad técnica, no rellenado con datos inventados.

---

## Ver la demo

**Sitio publicado en GitHub Pages:** [https://garielessga.github.io/FOXIT-CAPA-RAZABILIDAD/](https://garielessga.github.io/FOXIT-CAPA-RAZABILIDAD/)

La verificación de integridad corre directamente en el navegador mediante Web Crypto API (SHA-256). No necesita servidor ni cuenta.

---

## Ejecutar en local

Requiere **Node 22 o superior**. Sin dependencias externas: SQLite viene integrado (`node:sqlite`) y no hay que ejecutar `npm install`.

```bash
cd FOXIT-CAPA-RAZABILIDAD

# 1. Credenciales
copy .env.example .env     # en Linux/Mac: cp .env.example .env
#    Editar .env con FOXIT_CLIENT_ID y FOXIT_CLIENT_SECRET

# 2. Comprobar qué APIs responden de verdad
node diag_credenciales.mjs

# 3. Ejecutar el flujo completo (llama a Foxit y genera los documentos)
node run_complete_pipeline.js --no-tamper

# 4. Levantar la interfaz interactiva
node server.js            # http://localhost:3000
```

### Verificación de integridad, por separado

```bash
node verify_integrity.js              # todo el vault
node verify_integrity.js <sha256>     # un documento por su hash
```

Este script **no importa el motor de trazabilidad ni abre la base de datos**. Solo lee los archivos de `vault/` y comprueba que el contenido de cada uno coincida exactamente con el hash SHA-256 que le da nombre. Es reproducible con cualquier herramienta criptográfica estándar:

```bash
sha256sum vault/*.pdf
```

### Regenerar el sitio estático

```bash
node export_static.mjs                # escribe site/data.json, site/MANIFEST.json y copia a site/vault/
```

`site/index.html` es **código fuente**, no salida: el export no lo borra.

---

## Las dos formas de despliegue

### A. GitHub Pages — estático (despliegue en la web)

El sitio no ejecuta Node. `export_static.mjs` convierte el estado del motor a `site/data.json` y copia los PDFs al repositorio en `site/vault/`.

La verificación de integridad la hace **el navegador**, con Web Crypto SHA-256, sobre los bytes reales de cada archivo. Sigue siendo una verificación criptográfica real e independiente; lo que cambia es quién la ejecuta: en la versión con servidor era un proceso backend; aquí es quien abre la página (auditor o magistrado).

Es un argumento a favor, no una limitación: **es exactamente el escenario que el proyecto defiende**, un tercero que audita sin necesidad de credenciales de escritura ni servidores propietarios.

### B. Sistema local o en nube con backend

`server.js` es un servidor HTTP nativo: registra documentos, verifica, simula ataques reales en vivo y expone la API REST. Requiere disco persistente, porque SQLite y `vault/` residen en disco.

| Entorno | Notas |
|---|---|
| **Local** | `node server.js` en el puerto 3000. Funciona nativo. |
| **Render / Railway / Fly.io** | Soportan disco persistente o volumen montado. Desplegar con el repo y configurar variables de entorno. |
| **Vercel** | Requiere mover el vault a Vercel Blob y SQLite a Postgres debido al sistema de archivos efímero serverless. |

---

## Qué está verificado y qué no

Este proyecto no afirma nada que no se haya probado rigurosamente. La tabla completa está en [`02_SOLUCION_FOXIT/07_ACCESO_A_FOXIT.md`](02_SOLUCION_FOXIT/07_ACCESO_A_FOXIT.md).

| Afirmación | Estado |
|---|---|
| Document Generation genera PDFs desde plantillas `.docx` | **PROBADO** con llamadas reales a Foxit API |
| PDF Services sube, convierte y descarga | **PROBADO**, los 4 endpoints operativos |
| Hash SHA-256 detecta alteración de un byte | **PROBADO** |
| La cadena de auditoría detecta eventos alterados | **PROBADO** |
| Un tercero verifica sin la base de datos | **PROBADO** |
| eSign con estas credenciales | **FALLA** — `invalid_client` (cuenta requiere plan eSign específico) |
| eSign con credenciales válidas de Foxit eSign | **PENDIENTE** — requiere portal eSign comercial |

---

## Sobre Foxit eSign

Foxit separa arquitectónicamente el portal de firma electrónica del portal de PDF Services / Document Generation. Las credenciales actuales (`foxit_PKWrlh...`) pertenecen al portal de desarrollo **Document Generation y PDF Services** (`na1.fusion.foxit.com`), y al presentarlas en el endpoint de autenticación OAuth de Foxit eSign responden:

```json
{ "error": "invalid_client", "error_description": "invalid consumer credentials" }
```

Para habilitar eSign de forma nativa se requiere contratar o activar la suite en [developer-api.foxit.com/esign](https://developer-api.foxit.com/esign) y configurar `FOXIT_ESIGN_CLIENT_ID` y `FOXIT_ESIGN_CLIENT_SECRET`.

**Principio de honestidad:** El motor **no fabrica firmas ficticias** ni genera identificadores simulados en la base de datos. Cuando no hay credenciales eSign activas, el estado de firma se registra como `UNAVAILABLE` con su justificación técnica explícita.

---

## Seguridad

- `.env` está estrictamente ignorado en `.gitignore` y **nunca se versiona**.
- Las credenciales sensibles no están cableadas en el código fuente.
- Protección contra path traversal implementada en las rutas de descarga de archivos.
