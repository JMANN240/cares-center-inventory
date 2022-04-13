let urlsafe_b64encode = (string) => {
    console.log(string);
    return btoa(string.replace(/\//g, '_').replace(/\+/g, '-'))
}

let urlsafe_b64decode = (base64) => {
    return atob(base64).replace(/_/g, '/').replace(/-/g, '+')
}

let getProp = (prop) => {
    return x => x[prop];
}

let setCookie = (cookie_name, cookie_value, max_age=31536000) => {
    document.cookie = `${cookie_name}=${cookie_value};max-age=${max_age};samesite=strict`
}

let getCookie = (cookie_name) => {
    const match = document.cookie.match(`${cookie_name}=(.*?)(?:;|$)`);
    if (match == null) {
        return "";
    } else {
        return match[1];
    }
}

let timestampToFormatted = (timestamp) => {
    const dt = new Date(timestamp*1000);
    return `${dt.getHours()}:${dt.getMinutes().toString().padStart(2, '0')}:${dt.getSeconds().toString().padStart(2, '0')}, ${dt.getMonth()}/${dt.getDay()}/${dt.getFullYear()}`
}