const name_search_input = document.querySelector('#name-input');
const qty_search_input = document.querySelector('#qty-input');
const donor_search_input = document.querySelector('#donor-input');
const points_search_input = document.querySelector('#points-input');

const apply_button = document.querySelector('#apply');

const items_div = document.querySelector('#items');

let global_items = [];

let donors = [];
let donors_by_id = {};

let validate_inputs = () => {
    const create_name_input = document.querySelector('#create-name-input');
    const create_qty_input = document.querySelector('#create-qty-input');
    const create_points_input = document.querySelector('#create-points-input');

    if (create_name_input.value == '') {
        create_name_input.classList.add("bad-flash");
        setTimeout(() => {
            create_name_input.classList.remove("bad-flash");
        }, 1000);
        return false;
    }
    
    if (create_qty_input.value == '') {
        create_qty_input.classList.add("bad-flash");
        setTimeout(() => {
            create_qty_input.classList.remove("bad-flash");
        }, 1000);
        return false;
    }
    
    if (create_points_input.value == '') {
        create_points_input.classList.add("bad-flash");
        setTimeout(() => {
            create_points_input.classList.remove("bad-flash");
        }, 1000);
        return false;
    }

    return true;
}

let filter_items = (items) => {
    const filtered_items = items.filter((item) => {
        const name_matches = item.item_name.toLowerCase().includes(name_search_input.value.toLowerCase());
        const qty_matches = item.item_quantity == parseInt(qty_search_input.value) || qty_search_input.value == '';
        const donor_matches = donors_by_id[item.donor_id].toLowerCase().includes(donor_search_input.value.toLowerCase());
        const points_matches = item.item_points == parseInt(points_search_input.value) || points_search_input.value == '';
        return name_matches && qty_matches && donor_matches && points_matches;
    });
    return filtered_items
}

let constructAddItemDOMElement = () => {
    const item_entry_div = document.createElement('div');
    item_entry_div.classList.add('item-entry', 'flex', 'row', 'even');

    const item_name_input = document.createElement('input');
    item_name_input.type = 'text';
    item_name_input.placeholder = "Name";
    item_name_input.id = 'create-name-input';

    const item_qty_input = document.createElement('input');
    item_qty_input.type = 'text';
    item_qty_input.placeholder = "Qty";
    item_qty_input.id = 'create-qty-input';

    let new_item_quantity;

    item_qty_input.addEventListener('input', (e) => {
        const matches = item_qty_input.value.match(/^\d*\.?\d*$/g);
        console.log(matches);
        if (matches == null) {
            item_qty_input.value = new_item_quantity;
        } else {
            new_item_quantity = item_qty_input.value;
        }
    });

    const item_donor_select = document.createElement('select');
    for (const donor of donors) {
        const donor_option = document.createElement('option');
        donor_option.value = donor.donor_id;
        donor_option.innerHTML = donor.donor_name;

        item_donor_select.appendChild(donor_option);
    }
    item_donor_select.id = 'create-donor-input';

    const item_points_input = document.createElement('input');
    item_points_input.type = 'text';
    item_points_input.placeholder = "Points";
    item_points_input.id = 'create-points-input';

    const create_item_button = document.createElement('button');
    create_item_button.id = 'create-item';
    create_item_button.innerHTML = "Create";

    create_item_button.addEventListener('click', async () => {
        if (!validate_inputs()) return false;

        const res = await fetch('/api/item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_name: item_name_input.value,
                item_points: item_points_input.value,
                item_quantity: item_qty_input.value,
                donor_id: item_donor_select.value
            })
        });

        init();
    });

    item_entry_div.appendChild(item_name_input);
    item_entry_div.appendChild(item_qty_input);
    item_entry_div.appendChild(item_donor_select);
    item_entry_div.appendChild(item_points_input);
    item_entry_div.appendChild(create_item_button);

    return item_entry_div;
}

let draw_items = () => {
    items_div.innerHTML = "";

    items_div.appendChild(constructAddItemDOMElement());

    for (const item of global_items) {

        if (!filter_items(global_items).includes(item)) continue;

        const item_entry_div = document.createElement('div');
        item_entry_div.classList.add('item-entry', 'flex', 'row', 'even');

        const item_name_input = document.createElement('input');
        item_name_input.type = 'text';
        item_name_input.placeholder = "Name";
        item_name_input.value = item.item_name;

        item_name_input.addEventListener('input', (e) => {
            item.item_name = item_name_input.value;
        });

        const item_qty_input = document.createElement('input');
        item_qty_input.type = 'text';
        item_qty_input.placeholder = "Qty";
        item_qty_input.value = item.item_quantity;

        item_qty_input.addEventListener('input', (e) => {
            const matches = item_qty_input.value.match(/^\d*\.?\d*$/g);
            if (matches == null) {
                item_qty_input.value = item.item_quantity;
            } else {
                item.item_quantity = parseInt(item_qty_input.value);
            }
        });

        const item_donor_select = document.createElement('select');
        for (const donor of donors) {
            const donor_option = document.createElement('option');
            donor_option.value = donor.donor_id;
            donor_option.innerHTML = donor.donor_name;
            donor_option.selected = donor.donor_id == item.donor_id;

            item_donor_select.appendChild(donor_option);
        }

        item_donor_select.addEventListener('change', (e) => {
            item.donor_id = parseInt(item_donor_select.value);
        });

        const item_points_input = document.createElement('input');
        item_points_input.type = 'text';
        item_points_input.placeholder = "Points";
        item_points_input.value = item.item_points;

        item_points_input.addEventListener('input', (e) => {
            const matches = item_points_input.value.match(/^\d*\.?\d*$/g);
            if (matches == null) {
                item_points_input.value = item.item_points;
            } else {
                item.item_points = parseInt(item_points_input.value);
            }
        });

        const item_barcode_image = document.createElement('img');
        item_barcode_image.src = `/api/barcode?data=${item.item_barcode}`

        item_entry_div.appendChild(item_name_input);
        item_entry_div.appendChild(item_qty_input);
        item_entry_div.appendChild(item_donor_select);
        item_entry_div.appendChild(item_points_input);
        item_entry_div.appendChild(item_barcode_image);

        items_div.appendChild(item_entry_div);
    }
}

name_search_input.addEventListener('input', draw_items);
qty_search_input.addEventListener('input', draw_items);
donor_search_input.addEventListener('input', draw_items);
points_search_input.addEventListener('input', draw_items);

apply_button.addEventListener('click', async (e) => {
    for (const item of global_items) {
        const res = await fetch('/api/item', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_id: item.item_id,
                item_name: item.item_name,
                item_points: item.item_points,
                item_quantity: item.item_quantity,
                donor_id: item.donor_id,
                item_barcode: item.item_barcode
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
    donors = await donors_res.json();

    donors_by_id = {};
    for (const donor of donors) {
        donors_by_id[donor.donor_id] = donor.donor_name;
    }

    let items_res = await fetch("/api/item");
    global_items = await items_res.json();

    draw_items(global_items, donors)
}

init();