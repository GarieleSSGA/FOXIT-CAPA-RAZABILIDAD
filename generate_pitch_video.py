"""
Generador del Video Pitch Ejecutivo para Teddy y el Foxit Leadership Team.
Crea diapositivas de alta resolución (1920x1080) con diseño limpio (fondo blanco, naranja Foxit)
mostrando los documentos policiales concretos y cómo viajan entre etapas con Foxit.
Compila con FFmpeg a MP4 (H.264 / AAC).
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "pitch_frames"
VIDEO_OUTPUT = os.path.join("site", "video_pitch_foxit_leadership.mp4")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("site", exist_ok=True)

WIDTH, HEIGHT = 1920, 1080

# Colores de la paleta blanca y naranja Foxit
BG_COLOR = (248, 250, 252)       # #f8fafc
WHITE = (255, 255, 255)
FOXIT_ORANGE = (255, 55, 0)       # #ff3700
FOXIT_DARK = (194, 65, 12)        # #c2410c
FOXIT_SOFT = (255, 244, 240)      # #fff4f0
TEXT_DARK = (15, 23, 42)          # #0f172a
TEXT_MUTED = (100, 116, 139)      # #64748b
BORDER_COLOR = (226, 232, 240)    # #e2e8f0
BAD_RED = (220, 38, 38)
OK_GREEN = (22, 163, 74)
BLUE_INFO = (2, 132, 199)

def get_font(size, bold=False):
    # Intentar fuentes de Windows limpias
    fonts = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    for f in fonts:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except:
                pass
    return ImageFont.load_default()

def draw_header(draw, title, subtitle, kicker="FOXIT EXECUTIVE PITCH · PROPOSAL TO LEADERSHIP TEAM"):
    # Barra superior blanca
    draw.rectangle([0, 0, WIDTH, 120], fill=WHITE, outline=BORDER_COLOR, width=1)
    
    # Badge Foxit
    draw.rounded_rectangle([60, 36, 210, 84], radius=8, fill=FOXIT_ORANGE)
    font_badge = get_font(20, bold=True)
    draw.text((78, 48), "FOXIT API", font=font_badge, fill=WHITE)
    
    # Kicker y Título
    font_k = get_font(14, bold=True)
    draw.text((230, 36), kicker, font=font_k, fill=FOXIT_DARK)
    
    font_sub = get_font(18, bold=False)
    draw.text((230, 64), subtitle, font=font_sub, fill=TEXT_MUTED)
    
    # Badge lateral
    font_tag = get_font(14, bold=True)
    draw.rounded_rectangle([WIDTH - 380, 42, WIDTH - 60, 82], radius=20, fill=FOXIT_SOFT, outline=FOXIT_ORANGE, width=1)
    draw.text((WIDTH - 360, 52), "CONFIDENTIAL · PREPARED FOR TEDDY", font=font_tag, fill=FOXIT_ORANGE)

def draw_footer(draw, page_num, total_pages=7):
    draw.rectangle([0, HEIGHT - 60, WIDTH, HEIGHT], fill=WHITE, outline=BORDER_COLOR, width=1)
    font_f = get_font(15, bold=False)
    draw.text((60, HEIGHT - 42), "Document Traceability Layer for Criminal Justice & Public Sector · Verified with Foxit APIs", font=font_f, fill=TEXT_MUTED)
    draw.text((WIDTH - 180, HEIGHT - 42), f"Slide {page_num} of {total_pages}", font=font_f, fill=TEXT_MUTED)

# ==============================================================
# SLIDE 1: PORTADA EJECUTIVA
# ==============================================================
def render_slide_1():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "", "Proposal for Leadership Team Review", kicker="PROJECT SELECTION ROUND · FIRST PROPOSAL")
    
    # Card central
    draw.rounded_rectangle([100, 180, WIDTH - 100, HEIGHT - 100], radius=16, fill=WHITE, outline=BORDER_COLOR, width=2)
    
    # Línea decorativa naranja
    draw.rectangle([100, 180, 116, HEIGHT - 100], fill=FOXIT_ORANGE)
    
    font_tag = get_font(18, bold=True)
    draw.text((160, 240), "LEGAL TECH & PUBLIC SECTOR MODERNIZATION", font=font_tag, fill=FOXIT_ORANGE)
    
    font_main = get_font(52, bold=True)
    draw.text((160, 280), "Capa de Trazabilidad Documental Penal", font=font_main, fill=TEXT_DARK)
    draw.text((160, 350), "Transformando la Justicia con las APIs de Foxit", font=font_main, fill=FOXIT_DARK)
    
    font_desc = get_font(24, bold=False)
    desc_text = (
        "Una solución integral que erradica la pérdida de expedientes, los vencimientos de plazos sin responsable\n"
        "y la manipulación de pruebas en el proceso penal peruano (NCPP & D.Leg. 1735).\n"
        "Respaldado por Foxit Document Generation, PDF Services y Sellado Criptográfico SHA-256."
    )
    draw.text((160, 450), desc_text, font=font_desc, fill=TEXT_MUTED)
    
    # Grid de 3 pilares ejecutivos
    pills = [
        ("1. EVIDENCIA POLICIAL CONCRETA", "Acta de intervención, detención, incautación y cadena de custodia blindadas."),
        ("2. LLAMADAS REALES A FOXIT", "Generación real de PDFs con plantilla docx verificable en cuenta developer."),
        ("3. ESCALABILIDAD MASIVA", "Expansión inmediata a Cortes de Justicia, Fiscalías y Gobiernos Municipales.")
    ]
    for idx, (title, sub) in enumerate(pills):
        x = 160 + idx * 540
        draw.rounded_rectangle([x, 660, x + 500, 840], radius=12, fill=FOXIT_SOFT, outline=BORDER_COLOR, width=1)
        font_p_title = get_font(18, bold=True)
        draw.text((x + 24, 690), title, font=font_p_title, fill=FOXIT_DARK)
        font_p_sub = get_font(15, bold=False)
        draw.text((x + 24, 730), sub, font=font_p_sub, fill=TEXT_DARK)
        
    draw_footer(draw, 1)
    return img

# ==============================================================
# SLIDE 2: EL PROBLEMA REAL EN CIFRAS
# ==============================================================
def render_slide_2():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "", "Diagnóstico Forense: Por qué el papel colapsa la justicia penal")
    
    draw.rounded_rectangle([100, 160, WIDTH - 100, HEIGHT - 100], radius=16, fill=WHITE, outline=BORDER_COLOR, width=1)
    
    font_title = get_font(34, bold=True)
    draw.text((150, 200), "El Expediente Físico en Papel: Sin Dueño, Sin Reloj, Sin Memoria", font=font_title, fill=TEXT_DARK)
    
    # 4 Cuadros de dolor del sistema actual
    problems = [
        ("48 HORAS DE FLAGRANCIA", "El plazo corre en un cuaderno o en la memoria. Si vence sin acusación, el sospechoso queda libre por Hábeas Corpus y nadie responde.", BAD_RED),
        ("RUPTURA DE CUSTODIA", "Rótulos adhesivos en bolsas manuales. Si la hora discrepa con el oficio, la prueba se excluye del juicio por ilicitud procesal.", BAD_RED),
        ("TRAMO POLICÍA ➔ FISCALÍA", "El expediente viaja en moto con un mensajero. Si se extravía o se demora 6 horas en mesa de partes, nadie tiene la custodia formal.", BAD_RED),
        ("BORRADO DE HISTORIAL", "Al subsanar un error de placa, la policía destruye el acta original y la reemplaza. En juicio, la contradicción destruye el caso.", BAD_RED)
    ]
    
    for idx, (head, text, color) in enumerate(problems):
        r = idx // 2
        c = idx % 2
        x = 150 + c * 820
        y = 280 + r * 280
        draw.rounded_rectangle([x, y, x + 780, y + 240], radius=12, fill=BG_COLOR, outline=BORDER_COLOR, width=1)
        draw.rectangle([x, y, x + 10, y + 240], fill=color)
        
        draw.text((x + 30, y + 25), head, font=get_font(20, bold=True), fill=color)
        draw.text((x + 30, y + 70), text, font=get_font(18, bold=False), fill=TEXT_DARK)
        
    draw_footer(draw, 2)
    return img

# ==============================================================
# SLIDE 3: LOS DOCUMENTOS POLICIALES CONCRETOS (PEDIDO DE TEDDY)
# ==============================================================
def render_slide_3():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "", "Respuesta a Teddy: Especificidad en la Documentación Policial")
    
    draw.rounded_rectangle([100, 160, WIDTH - 100, HEIGHT - 100], radius=16, fill=WHITE, outline=BORDER_COLOR, width=1)
    
    draw.text((150, 190), "Los 6 Documentos Policiales Concretos Blindados por Foxit", font=get_font(32, bold=True), fill=TEXT_DARK)
    draw.text((150, 235), "Cada instrumento es generado con Foxit Document Generation y sellado al nacer con hash SHA-256 inmutable.", font=get_font(18, bold=False), fill=TEXT_MUTED)
    
    docs = [
        ("1. Acta de Intervención Policial (Flagrancia)", "Registra fecha, hora exacta (T0), lugar de intervención, sospechosos y especies.", "Foxit DocGen · Hash cdcd7e6b..."),
        ("2. Acta de Notificación de Detención y Derechos", "Garantía procesal (Art. 71 NCPP). Acredita que se comunicó el motivo de arresto.", "Foxit DocGen · Sello de Integridad"),
        ("3. Acta de Registro Personal e Incautación", "Inventario exhaustivo de especies sustraídas (teléfonos, billeteras, vehículo).", "Foxit DocGen · Vinculación Criptográfica"),
        ("4. Formato Oficial de Cadena de Custodia (Rótulo A-6)", "Embalaje y lacrado de evidencia material. Asocia perito responsable.", "Foxit PDF Services · Rótulo Inalterable"),
        ("5. Acta de Declaración del Imputado", "Manifestación policial con presencia de abogado defensor o defensor público.", "Foxit PDF Services · Línea de Tiempo"),
        ("6. Informe Policial de Remisión (Atestado)", "Oficio oficial que consolida el atestado completo para remisión al Fiscal.", "Foxit Transferencia TRF-0001 (Acuse)")
    ]
    
    for idx, (title, desc, tech) in enumerate(docs):
        r = idx // 2
        c = idx % 2
        x = 150 + c * 820
        y = 285 + r * 190
        
        draw.rounded_rectangle([x, y, x + 780, y + 165], radius=10, fill=WHITE, outline=BORDER_COLOR, width=1)
        draw.rectangle([x, y, x + 8, y + 165], fill=FOXIT_ORANGE)
        
        draw.text((x + 25, y + 18), title, font=get_font(18, bold=True), fill=TEXT_DARK)
        draw.text((x + 25, y + 54), desc, font=get_font(14, bold=False), fill=TEXT_MUTED)
        
        # Tag tech
        draw.rounded_rectangle([x + 25, y + 115, x + 400, y + 145], radius=6, fill=FOXIT_SOFT)
        draw.text((x + 35, y + 120), tech, font=get_font(12, bold=True), fill=FOXIT_ORANGE)

    draw_footer(draw, 3)
    return img

# ==============================================================
# SLIDE 4: CÓMO VIAJAN ENTRE ETAPAS USANDO FOXIT
# ==============================================================
def render_slide_4():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "", "Flujo de Etapa a Etapa: Cómo Intervienen las APIs de Foxit")
    
    draw.rounded_rectangle([100, 160, WIDTH - 100, HEIGHT - 100], radius=16, fill=WHITE, outline=BORDER_COLOR, width=1)
    
    draw.text((150, 195), "El Viaje del Expediente: De la Comisaría a la Sentencia Judicial", font=get_font(32, bold=True), fill=TEXT_DARK)
    
    stages = [
        ("ETAPA 1: COMISARÍA PNP", "Generación Digital Inmutable", "El oficial completa formulario normalizado.\nFoxit Document Generation inyecta variables en plantilla docx y emite PDF con hash SHA-256.", FOXIT_ORANGE),
        ("ETAPA 2: TRASLADO AL FISCAL", "Transferencia con Acuse Obligatorio", "Se abre tramo TRF-0001. El sistema exige firma y acuse digital de la Fiscalía. Si nadie confirma, salta alerta roja.", BLUE_INFO),
        ("ETAPA 3: FISCALÍA CORPORATIVA", "Versionado sin Destruir el Pasado", "Fiscal observa error de placa. Emite Disposición V1 y la PNP emite Acta V2 con Foxit. La V1 queda intacta en Bóveda.", OK_GREEN),
        ("ETAPA 4: JUZGADO DE CONTROL", "Auditoría en 30 Milisegundos", "El Juez abre el PDF y el navegador Web Crypto valida el hash SHA-256 de forma inmediata y pública.", FOXIT_DARK)
    ]
    
    for idx, (stage_title, sub, body, col) in enumerate(stages):
        x = 150 + idx * 405
        y = 280
        draw.rounded_rectangle([x, y, x + 380, y + 540], radius=12, fill=WHITE, outline=BORDER_COLOR, width=1)
        draw.rectangle([x, y, x + 380, y + 12], fill=col)
        
        draw.text((x + 20, y + 35), f"PASO {idx + 1}", font=get_font(14, bold=True), fill=col)
        draw.text((x + 20, y + 65), stage_title, font=get_font(17, bold=True), fill=TEXT_DARK)
        draw.text((x + 20, y + 105), sub, font=get_font(14, bold=True), fill=TEXT_MUTED)
        
        draw.line([x + 20, y + 140, x + 360, y + 140], fill=BORDER_COLOR, width=1)
        
        draw.text((x + 20, y + 165), body, font=get_font(15, bold=False), fill=TEXT_DARK)
        
    draw_footer(draw, 4)
    return img

# ==============================================================
# SLIDE 5: VALIDACIÓN REAL DE LAS LLAMADAS A FOXIT
# ==============================================================
def render_slide_5():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "", "Pruebas Reales: Estado Verificado en Foxit Developer Portal")
    
    draw.rounded_rectangle([100, 160, WIDTH - 100, HEIGHT - 100], radius=16, fill=WHITE, outline=BORDER_COLOR, width=1)
    
    draw.text((150, 195), "Llamadas Reales y Verificables a las APIs de Foxit", font=get_font(32, bold=True), fill=TEXT_DARK)
    
    # 2 Paneles
    draw.rounded_rectangle([150, 270, 900, 840], radius=12, fill=BG_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((180, 305), "✅ LO QUE ESTÁ 100% PROBADO Y EN PRODUCCIÓN", font=get_font(20, bold=True), fill=OK_GREEN)
    
    prov_text = (
        "• Foxit Document Generation API:\n"
        "  Generación real de Acta V1, Disposición Fiscal y Acta V2 desde plantillas .docx.\n"
        "  Tiempo promedio: 1,612 ms | Salida: PDFs válidos %PDF-1.4.\n\n"
        "• Foxit PDF Services API:\n"
        "  Flujo completo de 4 endpoints probado: upload, convert word-to-pdf, task polling y download.\n\n"
        "• Sello Criptográfico SHA-256:\n"
        "  El nombre del archivo ES su hash. Cambiar un solo byte rompe la verificación al instante.\n\n"
        "• Cadena de Auditoría de 9 Eventos:\n"
        "  Encadenamiento matemático de eventos procesales que impide borrar o insertar fojas."
    )
    draw.text((180, 360), prov_text, font=get_font(16, bold=False), fill=TEXT_DARK)
    
    # Panel derecho: honestidad en eSign
    draw.rounded_rectangle([940, 270, WIDTH - 150, 840], radius=12, fill=FOXIT_SOFT, outline=BORDER_COLOR, width=1)
    draw.text((970, 305), "ℹ️ TRANSPARENCIA TÉCNICA: FOXIT eSIGN", font=get_font(20, bold=True), fill=FOXIT_DARK)
    
    esign_text = (
        "• Foxit separa comercialmente el portal de desarrollo (Fusion)\n"
        "  del portal de firma electrónica corporativa (Foxit eSign).\n\n"
        "• Las credenciales de desarrollo responden formalmente:\n"
        "  {'error': 'invalid_client', 'error_description': 'invalid consumer credentials'}.\n\n"
        "• En lugar de inventar firmas ficticias para engañar al jurado,\n"
        "  nuestro motor declara honestamente el estado UNAVAILABLE\n"
        "  por requerir plan comercial enterprise.\n\n"
        "• La arquitectura tiene listo el conector OAuth2 para activar eSign\n"
        "  en el momento en que se provisione la cuenta comercial institucional."
    )
    draw.text((970, 360), esign_text, font=get_font(16, bold=False), fill=TEXT_DARK)

    draw_footer(draw, 5)
    return img

# ==============================================================
# SLIDE 6: ESCALABILIDAD A DISTRITOS Y MUNICIPALIDADES
# ==============================================================
def render_slide_6():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "", "Oportunidad de Mercado: Escalabilidad a todo el Sector Público")
    
    draw.rounded_rectangle([100, 160, WIDTH - 100, HEIGHT - 100], radius=16, fill=WHITE, outline=BORDER_COLOR, width=1)
    
    draw.text((150, 195), "De la Policía a las Municipalidades y Gobiernos Regionales", font=get_font(32, bold=True), fill=TEXT_DARK)
    draw.text((150, 240), "La fragilidad documental afecta a toda la administración del Estado. Foxit es la solución universal.", font=get_font(18, bold=False), fill=TEXT_MUTED)
    
    sectors = [
        ("MUNICIPALIDADES Y GOBIERNOS LOCALES", "Expedientes de Licencias de Obra y Habilitaciones Urbanas", "Extravío de planos y memorias descriptivas causa millones en arbitrajes. Foxit sella cada plano con metadata inalterable."),
        ("FISCALIZACIÓN TRIBUTARIA Y MULTAS", "Actas de Control, Notificaciones y Sanciones Administrativas", "Los infractores eluden multas alegando nulidad de notificación. Con Foxit cada acuse tiene hora certificada."),
        ("CONTRATACIONES PÚBLICAS Y LICITACIONES", "Trazabilidad de Bases, Propuestas y Adjudicaciones", "Cero sustitución de propuestas a medianoche. Transparencia auditable para la Contraloría General."),
        ("PODER JUDICIAL Y CORTES SUPERIORES", "Interoperabilidad Penal y Civil", "Conexión integral entre PNP, Fiscalía, Juzgados de Paz y Salas Penales.")
    ]
    
    for idx, (title, sub, body) in enumerate(sectors):
        r = idx // 2
        c = idx % 2
        x = 150 + c * 820
        y = 300 + r * 260
        draw.rounded_rectangle([x, y, x + 780, y + 220], radius=12, fill=WHITE, outline=BORDER_COLOR, width=1)
        draw.rectangle([x, y, x + 8, y + 220], fill=FOXIT_ORANGE)
        
        draw.text((x + 25, y + 22), title, font=get_font(18, bold=True), fill=FOXIT_DARK)
        draw.text((x + 25, y + 58), sub, font=get_font(15, bold=True), fill=TEXT_DARK)
        draw.text((x + 25, y + 105), body, font=get_font(15, bold=False), fill=TEXT_MUTED)
        
    draw_footer(draw, 6)
    return img

# ==============================================================
# SLIDE 7: CONCLUSIÓN Y LLAMADO A LA ACCIÓN
# ==============================================================
def render_slide_7():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "", "Propuesta de Decisión para Teddy y el Leadership Team")
    
    draw.rounded_rectangle([100, 160, WIDTH - 100, HEIGHT - 100], radius=16, fill=WHITE, outline=BORDER_COLOR, width=1)
    
    draw.text((150, 210), "¿Por qué este proyecto merece ser seleccionado?", font=get_font(38, bold=True), fill=TEXT_DARK)
    
    points = [
        ("1. FACTIBILIDAD Y PRESUPUESTO ALINEADOS", "El presupuesto propuesto es viable y realista. Toda la base técnica ya está funcionando con código Node 22 nativo."),
        ("2. DEMO INTERACTIVA SELF-SERVE YA DESPLEGADA", "El Leadership Team puede interactuar hoy mismo en vivo en GitHub Pages sin necesidad de instalar nada."),
        ("3. MÁXIMO IMPACTO PARA LA MARCA FOXIT", "Foxit no es solo un visor de PDFs: se posiciona como el estándar de confianza e integridad legal del Estado."),
        ("4. ESPECIFICIDAD NORMATIVA Y FORENSE", "El modelo contempla al detalle el Código Procesal Penal y la documentación policial real exigida.")
    ]
    
    for idx, (head, body) in enumerate(points):
        y = 300 + idx * 115
        draw.rounded_rectangle([150, y, WIDTH - 150, y + 95], radius=10, fill=BG_COLOR, outline=BORDER_COLOR, width=1)
        draw.text((180, y + 18), head, font=get_font(18, bold=True), fill=FOXIT_ORANGE)
        draw.text((180, y + 52), body, font=get_font(15, bold=False), fill=TEXT_DARK)
        
    draw.text((150, 780), "Listo para la Primera Ronda de Propuestas · Jueves 11:59 PM PST", font=get_font(20, bold=True), fill=FOXIT_DARK)
    draw.text((150, 815), "Demo en vivo: https://garielessga.github.io/FOXIT-CAPA-RAZABILIDAD/", font=get_font(16, bold=False), fill=TEXT_MUTED)
    
    draw_footer(draw, 7)
    return img

# ==============================================================
# COMPILACIÓN CON FFMPEG
# ==============================================================
def build_video():
    slides = [
        (render_slide_1(), 8),   # 8 segundos portada
        (render_slide_2(), 9),   # 9 segundos problema
        (render_slide_3(), 12),  # 12 segundos documentos policiales
        (render_slide_4(), 12),  # 12 segundos viaje etapa a etapa
        (render_slide_5(), 10),  # 10 segundos llamadas reales
        (render_slide_6(), 10),  # 10 segundos escalabilidad municipal
        (render_slide_7(), 9)    # 9 segundos conclusión y CTA
    ]
    
    frame_idx = 0
    fps = 25
    
    print("Renderizando frames de video a 1080p...")
    for slide_num, (img, duration_sec) in enumerate(slides, 1):
        num_frames = duration_sec * fps
        slide_path = os.path.join(OUTPUT_DIR, f"slide_{slide_num}.png")
        img.save(slide_path)
        print(f"  Slide {slide_num}: {duration_sec}s ({num_frames} frames)")
    
    # Crear archivo concat para ffmpeg
    concat_file = os.path.join(OUTPUT_DIR, "concat.txt")
    with open(concat_file, "w") as f:
        for slide_num, (_, duration_sec) in enumerate(slides, 1):
            slide_path = f"slide_{slide_num}.png"
            f.write(f"file '{slide_path}'\n")
            f.write(f"duration {duration_sec}\n")
        # El último frame debe repetirse según spec de concat demuxer
        f.write(f"file 'slide_{len(slides)}.png'\n")
        
    print("Compilando video con FFmpeg (libx264, 1080p)...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-vf", "format=yuv420p,fps=25",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        VIDEO_OUTPUT
    ]
    
    subprocess.run(cmd, check=True)
    print(f"\n¡VIDEO GENERADO EXITOSAMENTE!\nUbicación: {VIDEO_OUTPUT} ({os.path.getsize(VIDEO_OUTPUT) / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    build_video()
