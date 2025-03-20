<script>
    // Ajouter un événement de clic pour les boutons Like
    document.querySelectorAll('.like-btn').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Empêcher la soumission normale du formulaire

            // Enlever la classe "liked" de tous les autres boutons
            document.querySelectorAll('.like-btn').forEach(function(b) {
                b.classList.remove('liked');
            });

            // Ajouter la classe "liked" au bouton cliqué
            this.classList.add('liked');

            // Trouver l'index du plat pour envoyer l'action via le formulaire
            let platIndex = this.closest('form').querySelector('input[name="plat_index"]').value;

            // Créer un formulaire de soumission dynamique pour envoyer le vote
            let form = document.createElement('form');
            form.method = 'POST';
            form.action = '/vote/' + platIndex + '/like';  // Envoi du vote pour "like"
            
            // Soumettre le formulaire
            document.body.appendChild(form);
            form.submit();
        })
    });

    // Ajouter un événement de clic pour les boutons Dislike
    document.querySelectorAll('.dislike-btn').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Empêcher la soumission normale du formulaire

            // Enlever la classe "disliked" de tous les autres boutons
            document.querySelectorAll('.dislike-btn').forEach(function(b) {
                b.classList.remove('disliked');
            });

            // Ajouter la classe "disliked" au bouton cliqué
            this.classList.add('disliked');

            // Trouver l'index du plat pour envoyer l'action via le formulaire
            let platIndex = this.closest('form').querySelector('input[name="plat_index"]').value;

            // Créer un formulaire de soumission dynamique pour envoyer le vote
            let form = document.createElement('form');
            form.method = 'POST';
            form.action = '/vote/' + platIndex + '/dislike';  // Envoi du vote pour "dislike"
            
            // Soumettre le formulaire
            document.body.appendChild(form);
            form.submit();
        })
    });
</script>
