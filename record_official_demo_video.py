"""
Grabador y Productor del Video Pitch Oficial para Teddy y el Foxit Leadership Team.
1. Captura la INTERFAZ REAL Y OFICIAL de la demo (site/index.html) en resolución 1080p con Microsoft Edge headless.
2. Sintetiza locución oficial en español (Microsoft Sabina Desktop SAPI).
3. Sincroniza audio y video cuadro por cuadro.
4. Compila con FFmpeg en site/video_pitch_foxit_leadership.mp4 con pista de audio AAC.
"""

import os
import wave
import subprocess
import win32com.client

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SITE_DIR = os.path.join(BASE_DIR, "site")
OUTPUT_VIDEO = os.path.join(SITE_DIR, "video_pitch_foxit_leadership.mp4")
TEMP_DIR = os.path.join(BASE_DIR, "demo_capture_temp")
EDGE_EXE = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(SITE_DIR, exist_ok=True)

# 7 Escenas con guión de locución detallado y pedagógico
SCENES = [
    {
        "id": "1",
        "name": "Portada y Reloj de Flagrancia",
        "narration": (
            "Bienvenidos a la demostración oficial de la Capa de Trazabilidad Documental para el Proceso Penal, "
            "construida sobre las APIs de Foxit. En esta pantalla observamos el caso real EXP 2026 084 Lima por hurto agravado, "
            "con un reloj legal perentorio de 48 horas de flagrancia y las credenciales activas de Foxit Developer."
        )
    },
    {
        "id": "2",
        "name": "Dossier de Documentos Policiales Concretos",
        "narration": (
            "En respuesta al requerimiento de Teddy, presentamos el dossier completo de los seis instrumentos policiales oficiales. "
            "El acta de intervención en flagrancia, la notificación de detención y derechos, el registro personal e incautación, "
            "el rótulo oficial de cadena de custodia, la manifestación del imputado y el informe policial de remisión. "
            "Cada uno nace digitalizado con Foxit Document Generation y con un sello de integridad criptográfica inmutable."
        )
    },
    {
        "id": "3",
        "name": "Bosque Procesal Lado a Lado",
        "narration": (
            "Aquí observamos el Bosque Procesal con los dos árboles paralelos en simultáneo. "
            "A la izquierda, el árbol del régimen tradicional en papel con sus siete puntos críticos de ruptura donde se caen los juicios. "
            "A la derecha, el árbol blindado con Foxit, donde cada transferencia exige acuse de recibo y ningún plazo vence en silencio."
        )
    },
    {
        "id": "4",
        "name": "Inspección de Fase y Versionado Inmutable",
        "narration": (
            "Al inspeccionar la fase de subsanación, vemos cómo Foxit resuelve el mayor vicio procesal: "
            "cuando el fiscal detecta un error en la placa del vehículo incautado, en el sistema tradicional se destruye el acta original. "
            "Con Foxit aplicamos versionado inmutable: el fiscal emite su Disposición V1 y la policía genera el Acta V2. "
            "Ambas conviven intactas en la bóveda, preservando la verdad histórica."
        )
    },
    {
        "id": "5",
        "name": "Consola Dinámica de Foxit APIs",
        "narration": (
            "Esta consola interactiva permite al comité de liderazgo verificar la ejecución directa contra Foxit. "
            "Al pulsar invocar, la API Document Generation genera el documento oficial en mil seiscientos milisegundos con estatus doscientos OK. "
            "Asimismo, declaramos con honestidad técnica que el módulo de firma electrónica queda preparado para su plan comercial corporativo."
        )
    },
    {
        "id": "6",
        "name": "Bóveda Documental y Verificación Web Crypto",
        "narration": (
            "En la bóveda documental residen los tres PDFs sellados generados con Foxit. "
            "Cualquier juez, fiscal o auditor independiente puede verificar la autenticidad matemática en treinta milisegundos "
            "directamente en su navegador con Web Crypto SHA-256, sin necesidad de servidores propietarios ni permisos especiales."
        )
    },
    {
        "id": "7",
        "name": "Cadena de Auditoría y Escalabilidad",
        "narration": (
            "Los nueve eventos procesales forman una cadena matemática inquebrantable que enlaza el hash del hito anterior. "
            "Esta solución es 100% viable con el presupuesto propuesto y escala de inmediato a municipalidades y cortes de justicia. "
            "Foxit es el futuro de la documentación y trazabilidad para el Estado moderno. Muchas gracias."
        )
    }
]

def generate_audio(text, output_wav):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    # Seleccionar voz en español (Sabina o Helena)
    voices = speaker.GetVoices()
    for v in voices:
        desc = v.GetDescription()
        if "Sabina" in desc or "Helena" in desc or "Spanish" in desc:
            speaker.Voice = v
            break
            
    speaker.Rate = 0  # Velocidad natural
    filestream = win32com.client.Dispatch("SAPI.SpFileStream")
    filestream.Open(output_wav, 3, False)
    speaker.AudioOutputStream = filestream
    speaker.Speak(text)
    filestream.Close()
    
    with wave.open(output_wav, "rb") as f:
        duration = f.getnframes() / float(f.getframerate())
    return duration

def capture_official_demo_screen(scene_id, output_png):
    html_url = "file:///" + os.path.join(SITE_DIR, "index.html").replace("\\", "/") + f"?scene={scene_id}"
    edge_profile = os.path.join(TEMP_DIR, f"edge_prof_{scene_id}")
    os.makedirs(edge_profile, exist_ok=True)
    
    cmd = [
        EDGE_EXE,
        "--headless",
        "--disable-gpu",
        f"--user-data-dir={edge_profile}",
        "--window-size=1920,1080",
        "--virtual-time-budget=2000",
        f"--screenshot={output_png}",
        html_url
    ]
    subprocess.run(cmd, check=True)

def build_scene_clip(scene_idx, scene_data):
    sid = scene_data["id"]
    wav_path = os.path.join(TEMP_DIR, f"voice_scene_{sid}.wav")
    png_path = os.path.join(TEMP_DIR, f"screen_scene_{sid}.png")
    clip_mp4 = os.path.join(TEMP_DIR, f"clip_scene_{sid}.mp4")
    
    print(f"\n--- Procesando Escena {sid}: {scene_data['name']} ---")
    
    # 1. Audio
    duration = generate_audio(scene_data["narration"], wav_path)
    total_duration = duration + 1.2  # 1.2s de margen visual
    print(f"  Locución: {duration:.2f}s | Duración escena: {total_duration:.2f}s")
    
    # 2. Captura de pantalla de la demo oficial
    capture_official_demo_screen(sid, png_path)
    print(f"  Captura de pantalla oficial: {png_path} ({os.path.getsize(png_path)} bytes)")
    
    # 3. Compilar clip parcial con ffmpeg
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", png_path,
        "-i", wav_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", str(total_duration),
        "-shortest",
        clip_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  Clip de video compilado: {clip_mp4}")
    return clip_mp4

def main():
    print("=================================================================")
    print("PRODUCIENDO VIDEO OFICIAL DE LA DEMO CON AUDIO Y CAPTURAS REALES")
    print("=================================================================")
    
    clip_files = []
    for idx, s in enumerate(SCENES, 1):
        clip_path = build_scene_clip(idx, s)
        clip_files.append(clip_path)
        
    concat_list = os.path.join(TEMP_DIR, "concat_clips.txt")
    with open(concat_list, "w") as f:
        for c in clip_files:
            c_esc = c.replace("\\", "/")
            f.write(f"file '{c_esc}'\n")
            
    print("\nEnsamblando video final con FFmpeg...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "medium",
        OUTPUT_VIDEO
    ]
    subprocess.run(cmd_concat, check=True)
    
    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print("=================================================================")
    print(f"¡VIDEO OFICIAL COMPLETADO EXITOSAMENTE!")
    print(f"Archivo: {OUTPUT_VIDEO}")
    print(f"Tamaño: {size_mb:.2f} MB")
    print("=================================================================")

if __name__ == "__main__":
    main()
