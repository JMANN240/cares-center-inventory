let username_input = document.querySelector('#username');
let password_input = document.querySelector('#password');
let login_button = document.querySelector('#login');

let submitLogin = async () => {
    let res = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username_input.value,
            password: password_input.value
        })
    });
    let text = await res.text();
    if (res.status == 200) {
        window.location.href = '/';
    } else if (res.status == 406) {
        flash(text);
    }
}

login_button.addEventListener('click', submitLogin);

document.addEventListener('keydown', (e) => {
    if(e.key == 'Enter') {
        submitLogin();
    }
});