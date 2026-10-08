/**
 * Servidor web del MVP â€” Capa de trazabilidad Foxit.
 *
 *   node server.js
 *
 * Sin dependencias. Expone el estado del caso, las versiones selladas, la
 * cadena de auditorÃ­a, la verificaciÃ³n de integridad y los tramos de custodia
 * abiertos. Un tramo abierto significa que el expediente estÃ¡ con alguien que
 * todavÃ­a no confirmÃ³ recepciÃ³n: eso es lo que el papel no dice.
 */

import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { TraceabilityEngine, VAULT_DIR } from './traceability_engine.js';
import { loadEnv, esignStatus } from './config.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const env = loadEnv(__dirname);
const PORT = Number(env.PORT) || 3000;
const CASE_ID = env.DEMO_CASE_ID || 'CASE-2026-084';
const esign = esignStatus(env);

const engine = new TraceabilityEngine();

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.pdf': 'application/pdf',
  '.png': 'image/png',
  '.svg': 'image/svg+xml'
};

function sendJson(res, code, data) {
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*'
  });
  res.end(JSON.stringify(data, null, 2));
}

function sendFile(res, filePath, contentType) {
  if (!fs.existsSync(filePath)) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Archivo no encontrado');
    return;
  }
  res.writeHead(200, {
    'Content-Type': contentType,
    'Access-Control-Allow-Origin': '*'
  });
  fs.createReadStream(filePath).pipe(res);
}

function caseExists() {
  try {
    engine.getCase(CASE_ID);
    return true;
  } catch {
    return false;
  }
}

const server = http.createServer((req, res) => {
  const pathname = new URL(req.url, `http://${req.headers.host}`).pathname;

  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
    res.end();
    return;
  }

  if (!caseExists()) {
    sendJson(res, 503, {
      error: 'No hay caso de demostraciÃ³n.',
      hint: 'Ejecuta: node run_complete_pipeline.js'
    });
    return;
  }

  try {
    // Estado del caso y acceso a Foxit
    if (pathname === '/api/case' && req.method === 'GET') {
      const c = engine.getCase(CASE_ID);
      const start = new Date(c.created_at).getTime();
      const deadline = start + 48 * 3600 * 1000;
      sendJson(res, 200, {
        ...c,
        hoursRemaining: Math.max(0, deadline - Date.now()) / 3600000,
        deadline48h: new Date(deadline).toISOString(),
        openTransfers: engine.getOpenCustodyTransfers(CASE_ID),
        foxitAccess: {
          documentGeneration: true,
          pdfServices: true,
          eSign: esign.available,
          eSignNote: esign.note
        }
      });
      return;
    }

    // Versiones selladas, con su estado de firma real
    if (pathname === '/api/documents' && req.method === 'GET') {
      sendJson(res, 200, {
        versions: engine.getVersions(CASE_ID),
        institutions: engine.getInstitutions(),
        users: engine.getUsers()
      });
      return;
    }

    // Cadena de auditorÃ­a completa
    if (pathname === '/api/audit-trail' && req.method === 'GET') {
      sendJson(res, 200, { events: engine.getAuditTrail(CASE_ID), chain: engine.verifyChain(CASE_ID) });
      return;
    }

    // Tramos de custodia
    if (pathname === '/api/custody' && req.method === 'GET') {
      sendJson(res, 200, {
        chain: engine.getCustodyChain(CASE_ID),
        open: engine.getOpenCustodyTransfers(CASE_ID)
      });
      return;
    }

    // VerificaciÃ³n de integridad de una versiÃ³n
    if (pathname.startsWith('/api/verify/') && req.method === 'GET') {
      sendJson(res, 200, engine.verifyIntegrity(pathname.replace('/api/verify/', '')));
      return;
    }

    // VerificaciÃ³n de todo el caso: versiones + cadena
    if (pathname === '/api/verify' && req.method === 'GET') {
      sendJson(res, 200, engine.verifyAll(CASE_ID));
      return;
    }

    // Lineage de un documento: V1 -> V2
    if (pathname.startsWith('/api/lineage/') && req.method === 'GET') {
      sendJson(res, 200, { lineage: engine.getVersionLineage(pathname.replace('/api/lineage/', '')) });
      return;
    }

    // Ataque real, no simulado con un hash inventado.
    // Altera un byte del archivo sellado en el vault, verifica que el motor lo
    // detecte, y restaura el archivo. El evento queda en la cadena de auditorÃ­a:
    // la detecciÃ³n es genuine y el sistema vuelve a estar Ã­ntegro.
    if (pathname === '/api/simulate-tamper' && req.method === 'POST') {
      const version = engine.getVersions(CASE_ID).find((v) => v.version_number === 1);
      if (!version) {
        sendJson(res, 404, { error: 'No hay ninguna versiÃ³n V1 que atacar.' });
        return;
      }

      const vaultPath = path.join(VAULT_DIR, version.vault_filename);
      if (!fs.existsSync(vaultPath)) {
        sendJson(res, 404, { error: 'El archivo sellado no estÃ¡ en el vault.' });
        return;
      }

      const original = fs.readFileSync(vaultPath);
      const tampered = Buffer.from(original);
      tampered[tampered.length - 1] ^= 0xff; // un solo byte
      fs.writeFileSync(vaultPath, tampered);

      const detection = engine.verifyIntegrity(version.id);
      fs.writeFileSync(vaultPath, original); // restaurar

      const restored = engine.verifyIntegrity(version.id);

      sendJson(res, 200, {
        status: detection.status,
        detected: !detection.valid,
        originalHash: version.sha256,
        tamperedHash: detection.actualSha256,
        vaultFilename: version.vault_filename,
        message: detection.message,
        restoredAfterwards: restored.valid,
        chainStillIntact: engine.verifyChain(CASE_ID).valid,
        whatHappened:
          'Se alterÃ³ un byte del archivo sellado. El hash dejÃ³ de coincidir con el nombre del ' +
          'archivo, y el motor lo detectÃ³. DespuÃ©s se restaurÃ³ el archivo y la verificaciÃ³n volviÃ³ ' +
          'a pasar. El evento de detecciÃ³n quedÃ³ registrado en la cadena de auditorÃ­a.'
      });
      return;
    }

    // Documentos sellados, servidos desde el vault por hash
    if (pathname.startsWith('/vault/') && req.method === 'GET') {
      const hash = path.basename(pathname, '.pdf');
      if (!/^[0-9a-f]{64}$/.test(hash)) {
        sendJson(res, 400, { error: 'El nombre debe ser un hash SHA-256.' });
        return;
      }
      sendFile(res, path.join(VAULT_DIR, `${hash}.pdf`), 'application/pdf');
      return;
    }

    // EstÃ¡ticos y PDF sueltos en la raÃ­z
    const rel = pathname.replace(/^\/+/, '');
    if (rel.endsWith('.pdf')) {
      sendFile(res, path.join(__dirname, rel), 'application/pdf');
      return;
    }

    if (pathname === '/data.json' && req.method === 'GET') {
      const p = path.join(__dirname, 'site', 'data.json');
      sendFile(res, p, 'application/json; charset=utf-8');
      return;
    }

    const defaultPage = path.join(__dirname, 'site', 'index.html');
    const targetFile = pathname === '/' ? defaultPage : path.join(__dirname, pathname);
    if (fs.existsSync(targetFile) && fs.statSync(targetFile).isFile()) {
      sendFile(res, targetFile, MIME_TYPES[path.extname(targetFile)] || 'text/plain; charset=utf-8');
      return;
    }

    if (fs.existsSync(defaultPage)) {
      sendFile(res, defaultPage, 'text/html; charset=utf-8');
      return;
    }
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('404 Not Found');
  } catch (err) {
    sendJson(res, 400, { error: err.message });
  }
});

server.listen(PORT, () => {
  console.log(`${'='.repeat(72)}`);
  console.log(`SERVIDOR DE TRAZABILIDAD FOXIT â€” http://localhost:${PORT}`);
  console.log(`Caso: ${CASE_ID}`);
  console.log(`eSign: ${esign.available ? 'habilitado' : 'no habilitado en esta cuenta'}`);
  console.log(`${'='.repeat(72)}`);
});
