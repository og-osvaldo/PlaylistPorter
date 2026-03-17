import yt_dlp
import os

def descargar_musica():
    print("Descargador de Playlist")
    entrada = input("Pega el link aquí y presiona Enter: ")
    url = entrada.strip()
    
    if not url:
        print(" No existe Link.")
        return

    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': 'descargas/%(title)s.%(ext)s',
        'ffmpeg_location': './', 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'noplaylist': False,
    }

    try:
        print(f"\n--- Analizando: {url} ---")
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        print("\n ¡Música descargada y convertida a MP3!")
    except Exception as e:
        print(f"\n Error: {e}")

if __name__ == "__main__":
    if not os.path.exists('descargas'):
        os.makedirs('descargas')
    descargar_musica()