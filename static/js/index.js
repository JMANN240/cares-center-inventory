const logout_button = document.querySelector('#logout');

logout_button.addEventListener('click', async () => {
    let res = await fetch('/api/manager/logout', {
        method: 'POST'
    });
    window.location.href = window.location.href;
});