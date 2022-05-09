const logout_button = document.querySelector('#logout');

logout_button.addEventListener('click', async () => {
    await fetch('/api/logout', {
        method: 'POST'
    });
    window.location.href = window.location.href;
});