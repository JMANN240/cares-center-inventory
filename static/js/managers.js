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
        let username = document.createElement("div")
        username.classList.add("entry")
        username.innerHTML = manager.manager_name
        usernameColumn.appendChild(username)
    }
}

// add manager modal
var addModal = document.getElementById("add-modal");
var deleteModal = document.getElementById("delete-modal");
var box = document.getElementById("box");
var addBtn = document.getElementById("add-entry");
var deleteBtn = document.getElementById("delete-entry");
var submitBtn = document.getElementById("submit");
var confirmBtn = document.getElementById("confirm");
var closeAdd = document.getElementById("close-add");
var closeDelete = document.getElementById("close-delete");

// when the user clicks on the add manager button, open the modal
addBtn.onclick = function () {
    box.style.display = "none";
    addModal.style.display = "block";
    addBtn.style.display = "none";
    deleteBtn.style.display = "none";
}

deleteBtn.onclick = function () {
    box.style.display = "none";
    deleteModal.style.display = "block";
    addBtn.style.display = "none";
    deleteBtn.style.display = "none";
}

// close the modal
closeAdd.onclick = function () {
    addModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    deleteBtn.style.display = "inline-block";
}

closeDelete.onclick = function () {
    deleteModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    deleteBtn.style.display = "inline-block";
}


// add manager
submit.onclick = async () => {
    addModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    deleteBtn.style.display = "inline-block";
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

confirmBtn.onclick = function () {
    //need to capture input here Ty
    deleteModal.style.display = "none";
    box.style.display = "flex";
    addBtn.style.display = "inline-block";
    deleteBtn.style.display = "inline-block";

}