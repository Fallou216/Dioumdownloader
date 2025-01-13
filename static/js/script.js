document.getElementById('download-btn').addEventListener('click', async () => {
    const url = document.getElementById('video-url').value;
    const messageDiv = document.getElementById('message');

    if (!url) {
        messageDiv.textContent = "Veuillez entrer un lien valide.";
        return;
    }

    messageDiv.textContent = "Téléchargement en cours...";

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = `Téléchargement réussi ! Fichier : ${data.file}`;
        } else {
            messageDiv.textContent = `Erreur : ${data.error}`;
        }
    } catch (error) {
        messageDiv.textContent = "Erreur lors de la communication avec le serveur.";
    }
});
