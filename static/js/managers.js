const firstname_search_input = document.querySelector('#first-name-input');
const lastname_search_input = document.querySelector('#last-name-input');
const username_search_input = document.querySelector('#username-input');

const apply_button = document.querySelector('#apply');

const managers_div = document.querySelector('#managers');

let global_managers = [];

let validate_inputs = () => {
    const create_firstname_input = document.querySelector('#create-first-name-input');
    const create_lastname_input = document.querySelector('#create-last-name-input');
    const create_username_input = document.querySelector('#create-username-input');

    if (create_firstname_input.value == '') {
        create_firstname_input.classList.add("bad-flash");
        setTimeout(() => {
            create_firstname_input.classList.remove("bad-flash");
        }, 1000);
        return false;
    }
    
    if (create_lastname_input.value == '') {
        create_lastname_input.classList.add("bad-flash");
        setTimeout(() => {
            create_lastname_input.classList.remove("bad-flash");
        }, 1000);
        return false;
    }
    
    if (create_username_input.value == '') {
        create_username_input.classList.add("bad-flash");
        setTimeout(() => {
            create_username_input.classList.remove("bad-flash");
        }, 1000);
        return false;
    }

    return true;
}

let filter_managers = (managers) => {
    const filtered_managers = managers.filter((manager) => {
        const firstname_matches = manager.manager_firstname.toLowerCase().includes(firstname_search_input.value.toLowerCase());
        const lastname_matches = manager.manager_lastname.toLowerCase().includes(lastname_search_input.value.toLowerCase());
        const username_matches = manager.manager_username.toLowerCase().includes(username_search_input.value.toLowerCase());
        return firstname_matches && lastname_matches && username_matches;
    });
    return filtered_managers
}

let constructAddManagerDOMElement = () => {
    const manager_entry_div = document.createElement('div');
    manager_entry_div.classList.add('manager-entry', 'flex', 'row', 'even');

    const manager_firstname_input = document.createElement('input');
    manager_firstname_input.type = 'text';
    manager_firstname_input.placeholder = "First Name";
    manager_firstname_input.id = 'create-first-name-input';

    const manager_lastname_input = document.createElement('input');
    manager_lastname_input.type = 'text';
    manager_lastname_input.placeholder = "Last Name";
    manager_lastname_input.id = 'create-last-name-input';

    const manager_username_input = document.createElement('input');
    manager_username_input.type = 'text';
    manager_username_input.placeholder = "Username";
    manager_username_input.id = 'create-username-input';

    const manager_password_input = document.createElement('input');
    manager_password_input.type = 'password';
    manager_password_input.placeholder = "Password";
    manager_password_input.id = 'create-password-input';

    const is_active_div = document.createElement('div');
    is_active_div.classList.add('flex', 'column', 'centered');

    const is_active_h3 = document.createElement('h3');
    is_active_h3.classList.add('checkbox-label');
    is_active_h3.innerHTML = "Active"

    const is_active_input = document.createElement('input');
    is_active_input.type = 'checkbox';
    is_active_input.id = 'is-active-input';

    is_active_div.appendChild(is_active_h3);
    is_active_div.appendChild(is_active_input);

    const is_admin_div = document.createElement('div');
    is_admin_div.classList.add('flex', 'column', 'centered');

    const is_admin_h3 = document.createElement('h3');
    is_admin_h3.classList.add('checkbox-label');
    is_admin_h3.innerHTML = "Admin"

    const is_admin_input = document.createElement('input');
    is_admin_input.type = 'checkbox';
    is_admin_input.id = 'is-admin-input';

    is_admin_div.appendChild(is_admin_h3);
    is_admin_div.appendChild(is_admin_input);

    const create_manager_button = document.createElement('button');
    create_manager_button.id = 'create-manager';
    create_manager_button.innerHTML = "Create";

    create_manager_button.addEventListener('click', async () => {
        if (!validate_inputs()) return false;

        const res = await fetch('/api/manager/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                manager_firstname: manager_firstname_input.value,
                manager_lastname: manager_lastname_input.value,
                manager_username: manager_username_input.value,
                password: manager_password_input.value,
                is_active: is_active_input.checked,
                is_admin: is_admin_input.checked
            })
        });

        init();
    });

    manager_entry_div.appendChild(manager_firstname_input);
    manager_entry_div.appendChild(manager_lastname_input);
    manager_entry_div.appendChild(manager_username_input);
    manager_entry_div.appendChild(manager_password_input);
    manager_entry_div.appendChild(is_active_div);
    manager_entry_div.appendChild(is_admin_div);
    manager_entry_div.appendChild(create_manager_button);

    return manager_entry_div;
}

let draw_managers = () => {
    managers_div.innerHTML = "";

    managers_div.appendChild(constructAddManagerDOMElement());

    for (const manager of global_managers) {

        if (!filter_managers(global_managers).includes(manager)) continue;

        const manager_entry_div = document.createElement('div');
        manager_entry_div.classList.add('manager-entry', 'flex', 'row', 'even');

        const manager_firstname_input = document.createElement('input');
        manager_firstname_input.type = 'text';
        manager_firstname_input.placeholder = "First Name";
        manager_firstname_input.id = 'create-first-name-input';
        manager_firstname_input.value = manager.manager_firstname;

        manager_firstname_input.addEventListener('input', (e) => {
            manager.manager_firstname = manager_firstname_input.value;
        });

        const manager_lastname_input = document.createElement('input');
        manager_lastname_input.type = 'text';
        manager_lastname_input.placeholder = "Last Name";
        manager_lastname_input.id = 'create-last-name-input';
        manager_lastname_input.value = manager.manager_lastname;

        manager_lastname_input.addEventListener('input', (e) => {
            manager.manager_lastname = manager_lastname_input.value;
        });

        const manager_username_input = document.createElement('input');
        manager_username_input.type = 'text';
        manager_username_input.placeholder = "Username";
        manager_username_input.id = 'create-username-input';
        manager_username_input.value = manager.manager_username;

        manager_username_input.addEventListener('input', (e) => {
            manager.manager_username = manager_username_input.value;
        });

        const is_active_div = document.createElement('div');
        is_active_div.classList.add('flex', 'column', 'centered');

        const is_active_h3 = document.createElement('h3');
        is_active_h3.classList.add('checkbox-label');
        is_active_h3.innerHTML = "Active"

        const is_active_input = document.createElement('input');
        is_active_input.type = 'checkbox';
        is_active_input.id = 'is-active-input';
        is_active_input.checked = manager.is_active;

        is_active_input.addEventListener('change', (e) => {
            manager.is_active = is_active_input.checked;
        });

        is_active_div.appendChild(is_active_h3);
        is_active_div.appendChild(is_active_input);

        const is_admin_div = document.createElement('div');
        is_admin_div.classList.add('flex', 'column', 'centered');

        const is_admin_h3 = document.createElement('h3');
        is_admin_h3.classList.add('checkbox-label');
        is_admin_h3.innerHTML = "Admin"

        const is_admin_input = document.createElement('input');
        is_admin_input.type = 'checkbox';
        is_admin_input.id = 'is-admin-input';
        is_admin_input.checked = manager.is_admin;

        is_admin_input.addEventListener('change', (e) => {
            manager.is_admin = is_admin_input.checked;
        });

        is_admin_div.appendChild(is_admin_h3);
        is_admin_div.appendChild(is_admin_input);

        manager_entry_div.appendChild(manager_firstname_input);
        manager_entry_div.appendChild(manager_lastname_input);
        manager_entry_div.appendChild(manager_username_input);
        manager_entry_div.appendChild(is_active_div);
        manager_entry_div.appendChild(is_admin_div);

        managers_div.appendChild(manager_entry_div);
    }
}

firstname_search_input.addEventListener('input', draw_managers);
lastname_search_input.addEventListener('input', draw_managers);
username_search_input.addEventListener('input', draw_managers);

apply_button.addEventListener('click', async (e) => {
    for (const manager of global_managers) {
        const res = await fetch('/api/manager/update', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                manager_id: manager.manager_id,
                manager_firstname: manager.manager_firstname,
                manager_lastname: manager.manager_lastname,
                manager_username: manager.manager_username,
                passhash: manager.passhash,
                is_admin: manager.is_admin,
                is_active: manager.is_active
            })
        });
    }
    apply_button.classList.add("good-flash");
    setTimeout(() => {
        apply_button.classList.remove("good-flash");
    }, 1000);
});

let init = async () => {
    let manager_res = await fetch("/api/manager/read");
    global_managers = await manager_res.json();

    draw_managers()
}

init();