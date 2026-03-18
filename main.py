import yt_dlp
import os
import glob
import re

class MiLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg):
        if 'Video unavailable' in msg or 'not available' in msg:
            print("\n\033[91m⚠️  [AVISO] Canción no disponible (saltada).\033[0m")

def limpiar_titulo(titulo):
    patrones = [
        r'\(Official\s*Video\)', r'\(Video\s*Oficial\)', r'\(Lyric\s*Video\)', 
        r'\[HQ\]', r'\[4K\]', r'\[HD\]', r'Official\s*Music\s*Video', r'Video\s*Oficial'
    ]
    for p in patrones:
        titulo = re.sub(p, '', titulo, flags=re.IGNORECASE)
    return titulo.strip()

def generar_playlist_m3u8(directorio, nombre_p):
    ruta_m = os.path.join(directorio, f"00_{nombre_p}.m3u8")
    canciones = sorted(glob.glob(os.path.join(directorio, "*.mp3")))
    if canciones:
        with open(ruta_m, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for c in canciones:
                f.write(f"{os.path.basename(c)}\n")

def progreso_hook(d):
    if d['status'] == 'downloading':
        porcentaje = d.get('_percent_str', ' 0%')
        velocidad = d.get('_speed_str', 'N/A')
        total = d.get('_total_bytes_str', d.get('_total_bytes_estimate_str', 'N/A'))
        
        try:
            p_int = int(float(porcentaje.replace('%', '').strip()))
        except:
            p_int = 0
            
        barra = "█" * (p_int // 4) + "░" * (25 - (p_int // 4))
        print(f"\r\033[96m📥 [{barra}] {porcentaje} | 🚀 {velocidad} | 📦 {total}\033[0m   ", end='')
        
    elif d['status'] == 'finished':
        print("\n\033[92m✨ Descarga completa. Maximizando fidelidad de audio...\033[0m")

def limpiar_basura(directorio):
    for f in ('*.jpg', '*.png', '*.webp', '*.jpeg'):
        for a in glob.glob(os.path.join(directorio, "**", f), recursive=True):
            try: os.remove(a)
            except: pass

def descargar_musica():
    while True:
        print("\n\033[94m" + "═"*55)
        print("📥 TubeBeat ")
        print("═"*55 + "\033[0m")
        
        url = input("🔗 Pega el link de YouTube: ").strip()
        if not url: break

        print("\n📂 ¿Cómo guardar?")
        print("1. En una carpeta propia (Playlist)")
        print("2. Todo en carpeta general")
        op_carpeta = input("👉 Elige (1/2): ")
        
        print("\n🖼️  ¿Poner carátula a la canción?")
        print("1. Sí, poner carátula (1:1)")
        print("2. No, solo audio")
        op_arte = input("👉 Elige (1/2): ")

        ruta_base = 'descargas/%(playlist_title)s/%(title)s.%(ext)s' if op_carpeta == '1' else 'descargas/%(title)s.%(ext)s'

        opciones = {
            'format': 'bestaudio[ext=webm]/bestaudio/best',
            'outtmpl': ruta_base,
            'ignoreerrors': True,
            'logger': MiLogger(),
            'download_archive': 'historial_descargas.txt',
            'writethumbnail': op_arte == '1',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'},
                {'key': 'FFmpegMetadata', 'add_metadata': True}
            ],
            'progress_hooks': [progreso_hook],
            'quiet': True,
            'concurrent_fragment_downloads': 10, 
        }

        if op_arte == '1':
            opciones['postprocessors'].insert(1, {'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'})
            opciones['postprocessors'].insert(2, {'key': 'EmbedThumbnail'})
            opciones['postprocessor_args'] = {'thumbnailsconvertor': ['-vf', 'crop=ih:ih']}

        try:
            print("\n📡 Conectando con servidores de alta velocidad...")
            with yt_dlp.YoutubeDL(opciones) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if op_carpeta == '1' and info and 'entries' in info:
                    nombre_p = info.get('title', 'Playlist')
                    generar_playlist_m3u8(os.path.join('descargas', nombre_p), nombre_p)

            limpiar_basura('descargas')
            print("\033[92m✅ ¡Listo! Archivos optimizados en carpeta.\033[0m")

        except Exception as e:
            print(f"\n\033[91m❌ Error: {e}\033[0m")

        print("\n🔄 ¿Quieres descargar otro link?")
        print("1. Sí, continuar")
        print("2. No, salir")
        if input("👉 Elige (1/2): ") != '1':
            print("\n\033[94m👋 Cerrando TubeBeat... ¡Cambio y fuera!\033[0m"); break

if __name__ == "__main__":
    if not os.path.exists('descargas'): os.makedirs('descargas')
    descargar_musica()