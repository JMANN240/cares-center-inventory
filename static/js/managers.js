getManagers = async () => {
    // list of managers
    let managers_res = await fetch("/api/manager/read")
    let managers = await managers_res.json()
    // columns
    let firstNameColumn = document.getElementById("first-name-column")
    let lastNameColumn = document.getElementById("last-name-column")
    let usernameColumn = document.getElementById("username-column")
    // clear columns, in case there's leftover content
    while (firstNameColumn.firstChild) {
        firstNameColumn.removeChild(firstNameColumn.firstChild)
    }
    while (lastNameColumn.firstChild) {
        lastNameColumn.removeChild(lastNameColumn.firstChild)
    }
    while (usernameColumn.firstChild) {
        usernameColumn.removeChild(usernameColumn.firstChild)
    }
    // populate columns
    for (const manager of managers) {
        let username = document.createElement("div")
        username.classList.add("entry")
        username.innerHTML = manager.manager_name
        usernameColumn.appendChild(username)
    }
}

// add manager modal
var modal = document.getElementById("myModal");
var box = document.getElementById("box");
var addBtn = document.getElementById("add-entry");
var submitBtn = document.getElementById("submit");

// get the <span> element that closes the modal
var close = document.getElementById("close");

// when the user clicks on the add manager button, open the modal
addBtn.onclick = function () {
    box.style.display = "none";
    modal.style.display = "block";
    addBtn.style.opacity = 0;
}

// close the modal
close.onclick = function () {
    modal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.opacity = 100;
}

// add manager
submit.onclick = async () => {
    modal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.opacity = 100;
    // add a new manager
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value

    console.log(username)
    console.log(password)

    let res = await fetch("/api/manager/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            manager_name: username,
            password: password
        })
    })
    // update manager list
    getManagers()
}