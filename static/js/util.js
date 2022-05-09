const flash_div = document.querySelector('#flash');

let flash = (text, ms=10000) => {
    flash_div.style.display = "flex";
    flash_div.innerHTML = text;
    setTimeout(() => {
        flash_div.style.display = "none";
        flash_div.innerHTML = "";
    }, ms);
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
    return `${dt.getHours()}:${dt.getMinutes().toString().padStart(2, '0')}:${dt.getSeconds().toString().padStart(2, '0')}, ${dt.getMonth()+1}/${dt.getDate()}/${dt.getFullYear()}`
}