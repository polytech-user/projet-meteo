document.querySelector('form').addEventListener('submit', function(e) {
    const ca = parseFloat(document.getElementById('chiffre-affaire').value);
    const cf = parseFloat(document.getElementById('couts-fixes').value);
    
    // Réinitialiser les messages d'erreur
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    
    // Validation coûts fixes <= CA
    if (cf > ca) {
        e.preventDefault();
        const errorMsg = document.createElement('div');
        errorMsg.className = 'error-message';
        errorMsg.style.color = 'red';
        errorMsg.textContent = 'Les coûts fixes ne peuvent pas dépasser le chiffre d\'affaire';
        document.getElementById('couts-fixes').after(errorMsg);
    }
});