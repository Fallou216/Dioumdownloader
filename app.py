from flask import Flask, render_template, request, jsonify
import yt_dlp
import os
import subprocess

app = Flask(__name__)

# Mettre à jour yt-dlp
subprocess.run(['pip', 'install', '--upgrade', 'yt-dlp'])

# Dossier pour stocker les vidéos téléchargées
DOWNLOAD_FOLDER = os.path.join('static', 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Configuration de Flask pour servir les fichiers statiques
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/')
def index():
    """
    Route pour afficher la page principale.
    """
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    """
    Route pour télécharger une vidéo à partir d'un lien fourni (YouTube, TikTok, etc.)
    """
    try:
        # Récupérer les données JSON envoyées depuis le frontend
        data = request.get_json()
        video_url = data.get('url')

        # Vérifier si un lien est fourni
        if not video_url:
            return jsonify({'status': 'error', 'message': 'Aucun lien fourni.'}), 400

        # Options de téléchargement avec yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',  # Télécharger la meilleure qualité vidéo et audio
            'merge_output_format': 'mp4',  # Fusionner la vidéo et l'audio dans un fichier MP4
            'noplaylist': True,  # Pour éviter de télécharger une playlist entière
            'postprocessors': [{  # Utilisation de ffmpeg pour combiner la vidéo et l'audio
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Format de sortie souhaité
            }],
        }

        # Vérification spécifique pour TikTok
        if 'tiktok.com' in video_url:
            ydl_opts['outtmpl'] = os.path.join(DOWNLOAD_FOLDER, 'tiktok_%(id)s.%(ext)s')  # Nommage spécifique pour TikTok

        # Télécharger la vidéo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = os.path.basename(ydl.prepare_filename(info))  # Nom du fichier téléchargé

        # Obtenir le chemin complet du fichier téléchargé
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)

        # Retourner une réponse JSON avec le chemin complet
        return jsonify({
            'status': 'success',
            'message': 'Téléchargement réussi.',
            'file_path': file_path,
            'download_url': f"/static/downloads/{filename}"  # Lien direct vers le fichier
        })
    except Exception as e:
        # Gérer les erreurs et renvoyer une réponse JSON
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Lancer l'application Flask
    app.run(debug=True)
