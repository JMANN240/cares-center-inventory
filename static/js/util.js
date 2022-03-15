let urlsafe_b64encode = (string) => {
    console.log(string);
    return btoa(string.replace(/\//g, '_').replace(/\+/g, '-'))
}

let urlsafe_b64decode = (base64) => {
    return atob(base64).replace(/_/g, '/').replace(/-/g, '+')
}