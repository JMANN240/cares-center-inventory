const items_div = document.querySelector('#items');
const donors_div = document.querySelector('#donor-weights');
const student_id_input = document.querySelector('#student-id');
const submit_transaction_button = document.querySelector('#submit-transaction');
const total_points_display = document.querySelector('#total-points');

let items = [];

let donors = [];

let update_total_points_display = () => {
    points = 0;

    for (const item of items) {
        points += (item.quantity * item.points);
    }

    total_points_display.value = `Total Points: ${points}`;
}

let constructDonorWeightDOMElement = (donor) => {
    let donor_weight_div = document.createElement('div');
    donor_weight_div.classList.add("flex", "centered", "outlined", "donor-weight");

    let donor_name_h1 = document.createElement('h1');
    donor_name_h1.innerHTML = donor.name;
    donor_weight_div.appendChild(donor_name_h1);

    let donor_weight_input = document.createElement('input');
    donor_weight_input.type = "text";
    donor_weight_input.placeholder = "Lbs.";
    donor_weight_input.classList.add('big');
    donor_weight_input.size = 4;
    donor_weight_input.value = donor.weight ?? "";

    donor_weight_input.addEventListener('input', (e) => {
        const matches = donor_weight_input.value.match(/^\d*\.?\d*$/g);
        if (matches == null) {
            donor_weight_input.value = donor.weight;
        } else {
            donor.weight = donor_weight_input.value;
        }
    });

    donor_weight_div.appendChild(donor_weight_input);

    return donor_weight_div;
}

let constructItemDOMElement = (item) => {
    
    let item_div = document.createElement('div');

    item_div.classList.add("flex", "row", "even", "nowrap", "outlined", "item", "stretch");

    let info_div = document.createElement('div');
    let name_h1 = document.createElement('h1');
    name_h1.classList.add('big');
    name_h1.innerHTML = item.name;
    let donor_h1 = document.createElement('h1');
    donor_h1.classList.add('medium');
    donor_h1.innerHTML = item.donor.name;

    info_div.classList.add("flex", "column", "even");

    info_div.appendChild(name_h1);
    info_div.appendChild(donor_h1);

    let quantity_div = document.createElement('div');
    let increment_button = document.createElement('button');
    increment_button.innerHTML = '+';
    increment_button.classList.add("small", "flex", "centered");
    let quantity_h1 = document.createElement('h1');
    quantity_h1.classList.add('big', 'bordered');
    quantity_h1.innerHTML = item.quantity;
    let decrement_button = document.createElement('button');
    decrement_button.classList.add("small", "flex", "centered");
    decrement_button.innerHTML = '-';
    
    increment_button.addEventListener('click', (e) => {
        item.quantity+=1;
        update_total_points_display();
        drawItems();
    });
    
    decrement_button.addEventListener('click', (e) => {
        item.quantity-=1;
        update_total_points_display();
        if (item.quantity == 0) {
            items = items.filter(item => item.quantity > 0);
            const item_donors = items.map(item => item.donor.name);
            donors = donors.filter(donor => item_donors.includes(donor.name));
        }
        drawItems();
        drawDonorWeights();
    });

    quantity_div.classList.add("flex", "column", "even", 'centered');

    quantity_div.appendChild(increment_button);
    quantity_div.appendChild(quantity_h1);
    quantity_div.appendChild(decrement_button);

    let points_div = document.createElement('div');
    let points_h1 = document.createElement('h1');
    points_h1.classList.add('huge', 'bordered');
    points_h1.innerHTML = item.points;
    points_h1.classList.add("count");

    points_div.classList.add("flex", "column", "centered");

    points_div.appendChild(points_h1);

    item_div.appendChild(info_div);
    item_div.appendChild(quantity_div);
    item_div.appendChild(points_div);

    return item_div;
}

const addItem = async (barcode) => {
    barcode = barcode.match(/\d{7}/)[0];

    const barcodes = items.map(item => item.barcode);

    if (!barcodes.includes(barcode)) {

        let item_res = await fetch(`/api/items/barcode/${barcode}`);
        let item = await item_res.json();

        item.quantity = 1;

        items.push(item);
        update_total_points_display();
        drawItems();

        const donor_names = donors.map(donor => donor.name)

        if (!donor_names.includes(item.donor.name) && item.donor.weighs) {
            item.donor.weight = "";
            donors.push(item.donor)
        }

        drawDonorWeights();
    }
}

let onScanSuccess = addItem;

let drawItems = () => {
    items_div.innerHTML = "";
    for (let item of items) {
        items_div.appendChild(constructItemDOMElement(item))
    }
};

let drawDonorWeights = () => {
    donors_div.innerHTML = "";
    for (let donor of donors) {
        donors_div.appendChild(constructDonorWeightDOMElement(donor));
    }
};

let calculateQRBox = function(width, height) { 
    let min_dimension = Math.min(width, height);
    let scaled_dimension = min_dimension * 0.8;
    return { 
        width: scaled_dimension, 
        height: scaled_dimension 
    }; 
}

let html5Qrcode = new Html5Qrcode('reader');
html5Qrcode.start({ facingMode: 'environment' }, { fps: 10, qrbox: calculateQRBox }, onScanSuccess);

let validate_inputs = () => {
    if (items.length == 0) {
        flash("No items in transaction", 5000);
        items_div.classList.add("bad-flash");
        setTimeout(() => {
            items_div.classList.remove("bad-flash");
        }, 1000);
        return false;
    }

    for (const donor of donors) {
        if (donor.weight == "") {
            flash(`Missing ${donor.name}'s weight`, 5000);
            donors_div.classList.add("bad-flash");
            setTimeout(() => {
                donors_div.classList.remove("bad-flash");
            }, 1000);
            return false;
        }
    }

    const student_id = student_id_input.value;
    if (student_id == "") {
        flash("Missing student ID", 5000);
        student_id_input.classList.add("bad-flash");
        setTimeout(() => {
            student_id_input.classList.remove("bad-flash");
        }, 1000);
        return false;
    }

    return true;
}

submit_transaction_button.addEventListener('click', async () => {
    
    if (!validate_inputs()) return;

    const student_id = student_id_input.value;
    const manager_id = getCookie("manager_id");

    const res = await fetch('/api/transactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            student_id: student_id,
            manager_id: manager_id
        })
    });

    const transaction = await res.json()

    for (const item of items) {
        await fetch('/api/transactions/item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_id: item.id,
                transaction_id: transaction.id,
                quantity: item.quantity
            })
        });
    }

    for (const donor of donors) {
        await fetch('/api/transactions/weight', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                donor_id: donor.id,
                transaction_id: transaction.id,
                weight: donor.weight
            })
        });
    }

    window.location.href = '/';
});