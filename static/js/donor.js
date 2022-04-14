const name_search_input = document.querySelector('#name-input');
const donors_div = document.querySelector('#donors');
const apply_button = document.querySelector('#apply');

let global_donors = [];

let validate_inputs = () => {
    const create_name_input = document.querySelector('#create-name-input');

    if (create_name_input.value == '') {
        create_name_input.classList.add("bad-flash");
        setTimeout(() => {
            create_name_input.classList.remove("bad-flash");
        }, 1000);
        return false;
    }

    return true;
}

let filter_donors = (donors) => {
    const filtered_donors = donors.filter((donor) => {
        const name_matches = donor.donor_name.toLowerCase().includes(name_search_input.value.toLowerCase());
        return name_matches;
    });
    return filtered_donors
}

let constructAddDonorDOMElement = () => {
    const donor_entry_div = document.createElement('div');
    donor_entry_div.classList.add('donor-entry', 'flex', 'row', 'even');

    const donor_name_input = document.createElement('input');
    donor_name_input.type = 'text';
    donor_name_input.placeholder = "Name";
    donor_name_input.id = 'create-name-input';

    const create_donor_button = document.createElement('button');
    create_donor_button.id = 'create-donor';
    create_donor_button.innerHTML = "Create";

    create_donor_button.addEventListener('click', async () => {
        if (!validate_inputs()) return false;

        const res = await fetch('/api/donor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                donor_name: donor_name_input.value
            })
        });

        init();
    });

    donor_entry_div.appendChild(donor_name_input);
    donor_entry_div.appendChild(create_donor_button);

    return donor_entry_div;
}

let draw_donors = () => {
    donors_div.innerHTML = "";

    donors_div.appendChild(constructAddDonorDOMElement());

    for (const donor of global_donors) {

        if (!filter_donors(global_donors).includes(donor)) continue;

        const donor_entry_div = document.createElement('div');
        donor_entry_div.classList.add('donor-entry', 'flex', 'row', 'even');

        const donor_name_input = document.createElement('input');
        donor_name_input.type = 'text';
        donor_name_input.placeholder = "Name";
        donor_name_input.value = donor.donor_name;

        donor_name_input.addEventListener('input', (e) => {
            donor.donor_name = donor_name_input.value;
        });

        donor_entry_div.appendChild(donor_name_input);

        donors_div.appendChild(donor_entry_div);
    }
}

name_search_input.addEventListener('input', draw_donors);

apply_button.addEventListener('click', async (e) => {
    for (const donor of global_donors) {
        const res = await fetch('/api/donor', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                donor_id: donor.donor_id,
                donor_name: donor.donor_name
            })
        });
    }
    apply_button.classList.add("good-flash");
    setTimeout(() => {
        apply_button.classList.remove("good-flash");
    }, 1000);
});

let init = async () => {
    let donors_res = await fetch("/api/donor");
    global_donors = await donors_res.json();

    draw_donors();
}

init();