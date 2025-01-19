document.getElementById('back-button').addEventListener('click', function() {
    document.getElementById('confirmation-modal').style.display = 'block';
});

document.getElementById('confirm-back').addEventListener('click', function() {
    window.location.href = '/';
});

document.getElementById('cancel-back').addEventListener('click', function() {
    document.getElementById('confirmation-modal').style.display = 'none';
});
