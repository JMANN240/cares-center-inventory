getManagers = async () => {
    // list of managers
    let managers = await (await fetch("/api/manager/read")).json()
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
        console.log(manager);
        let firstname = document.createElement("div")
        firstname.classList.add("entry")
        firstname.innerHTML = manager.manager_firstname
        firstNameColumn.appendChild(firstname)
        let lastname = document.createElement("div")
        lastname.classList.add("entry")
        lastname.innerHTML = manager.manager_lastname
        lastNameColumn.appendChild(lastname)
        let username = document.createElement("div")
        username.classList.add("entry")
        username.innerHTML = manager.manager_username
        usernameColumn.appendChild(username)
    }
}

var box = document.getElementById("box");

// add manager nodes
var addModal = document.getElementById("add-modal");
var addBtn = document.getElementById("add-entry");
var addSubmitBtn = document.getElementById("add-submit");
var addClose = document.getElementById("add-close");

// deactivate manager nodes
var deactivateModal = document.getElementById("deactivate-modal");
var deactivateBtn = document.getElementById("deactivate-entry");
var deactivateSubmitBtn = document.getElementById("deactivate-submit");
var deactivateClose = document.getElementById("deactivate-close");

// when the user clicks on the add manager button, open the modal
addBtn.onclick = function () {
    box.style.display = "none";
    addModal.style.display = "block";
    addBtn.style.display = "none";
    deactivateBtn.style.display = "none";
}

deactivateBtn.onclick = function () {
    box.style.display = "none";
    deactivateModal.style.display = "block";
    addBtn.style.display = "none";
    deactivateBtn.style.display = "none";
}

// close the modal
addClose.onclick = function () {
    addModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    deactivateBtn.style.display = "inline-block";
}

deactivateClose.onclick = function () {
    deactivateModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    deactivateBtn.style.display = "inline-block";
}

// add manager
addSubmitBtn.onclick = async () => {
    addModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    deactivateBtn.style.display = "inline-block";
    // add a new manager
    let firstName = document.getElementById("add-first-name").value
    let lastName = document.getElementById("add-last-name").value
    let username = document.getElementById("add-username").value
    let password = document.getElementById("add-password").value

    if (firstName == "" || lastName == "" || username == "" || password == "") {
        // TODO: display red error text! some fields were left blank!!!
        return
    }

    let res = await fetch("/api/manager/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            manager_firstname: firstName,
            manager_lastname: lastName,
            manager_username: username,
            password: password
        })
    })
    // update manager list
    getManagers()
}

// deactivate manager
deactivateSubmitBtn.onclick = async () => {
    deactivateModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    deactivateBtn.style.display = "inline-block";

    let username = document.getElementById("deactivate-username").value

    if (username == "") {
        // TODO: display red error text! field was left blank!!!
        return
    }

    // we need more API routes before we can deactivate.
    //let res = await fetch("/api/manager")
}
