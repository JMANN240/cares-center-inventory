const params = new URLSearchParams(window.location.search)

let username_input = document.querySelector('#username');
let password_input = document.querySelector('#password');
let login_button = document.querySelector('#login');

let submitLogin = async () => {
    let res = await fetch('/api/manager/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username_input.value,
            password: password_input.value
        })
    });
    if (res.status == 200) {
        let redirect = params.get('redirect') ?? urlsafe_b64encode('/');
        redirect = urlsafe_b64decode(redirect);
        window.location.href = redirect;
    }
}

login_button.addEventListener('click', submitLogin);

document.addEventListener('keydown', (e) => {
    if(e.key == 'Enter') {
        submitLogin();
    }
});