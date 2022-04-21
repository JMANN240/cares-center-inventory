let firstNameColumn = document.getElementById("first-name-column")
let lastNameColumn = document.getElementById("last-name-column")
let usernameColumn = document.getElementById("username-column")
let activeColumn = document.getElementById("active-column")
let adminColumn = document.getElementById("admin-column")

getManagers = async () => {
    // list of managers
    let managers = await (await fetch("/api/manager/read")).json()
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
    while (activeColumn.firstChild) {
        activeColumn.removeChild(activeColumn.firstChild)
    }
    while (adminColumn.firstChild) {
        adminColumn.removeChild(adminColumn.firstChild)
    }
    // (re)populate columns
    for (i = 0; i < managers.length; ++i) {
        let firstname = document.createElement("div")
        firstname.classList.add("entry")
        firstname.innerHTML = managers[i].manager_firstname
        firstNameColumn.appendChild(firstname)
        let lastname = document.createElement("div")
        lastname.classList.add("entry")
        lastname.innerHTML = managers[i].manager_lastname
        lastNameColumn.appendChild(lastname)
        let username = document.createElement("div")
        username.classList.add("entry")
        username.innerHTML = managers[i].manager_username
        usernameColumn.appendChild(username)
        let active = document.createElement("input")
        active.classList.add("checkbox-entry")
        active.id = "active" + i
        active.type = "checkbox"
        active.checked = managers[i].is_active
        activeColumn.appendChild(active)
        let admin = document.createElement("input")
        admin.classList.add("checkbox-entry")
        admin.id = "admin" + i
        admin.type = "checkbox"
        admin.checked = managers[i].is_admin
        adminColumn.appendChild(admin)
    }
}

updateManagers = async () => {
    // list of managers. :)
    let managers = await (await fetch("/api/manager/read")).json()

    for (i = 0; i < managers.length; ++i) {
        let activeid = "active" + i
        let active = document.getElementById(activeid)
        let adminid = "admin" + i
        let admin = document.getElementById(adminid)

        // if the checkbox is different...
        if (active.checked != managers[i].is_active) {
            if (active.checked) {
                // activate
                let res = await fetch("/api/manager/activate?manager_id=" + managers[i].manager_id)
            } else {
                // deactivate
                let res = await fetch("/api/manager/deactivate?manager_id=" + managers[i].manager_id)
            }
        }

        // if the checkbox is different...
        if (admin.checked != managers[i].is_admin) {
            if (admin.checked) {
                // promote
                let res = await fetch("/api/manager/promote?manager_id=" + managers[i].manager_id)
            } else {
                // demote
                let res = await fetch("/api/manager/demote?manager_id=" + managers[i].manager_id)
            }
        }
    }
}

var box = document.getElementById("box");

// apply button
var applyBtn = document.getElementById("apply-button");

applyBtn.onclick = async function () {
    await updateManagers();
    await getManagers();
    applyBtn.classList.add("good-flash");
    setTimeout(() => {
        applyBtn.classList.remove("good-flash");
    }, 1000);
}

// add manager nodes
var addModal = document.getElementById("add-modal");
var addBtn = document.getElementById("add-entry");
var addSubmitBtn = document.getElementById("add-submit");
var addClose = document.getElementById("add-close");

// when the user clicks on the add manager button, open the modal
addBtn.onclick = function () {
    box.style.display = "none";
    addModal.style.display = "block";
    addBtn.style.display = "none";
    applyBtn.style.display = "none";
}

// close the modal
addClose.onclick = function () {
    addModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    applyBtn.style.display = "inline-block";
}

// add manager
addSubmitBtn.onclick = async () => {
    addModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    applyBtn.style.display = "inline-block";
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
