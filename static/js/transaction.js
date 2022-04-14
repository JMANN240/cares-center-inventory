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
        points += (item.transaction_quantity * item.item_points);
    }

    total_points_display.value = `Total Points: ${points}`;
}

let constructDonorWeightDOMElement = (donor) => {
    let donor_weight_div = document.createElement('div');
    donor_weight_div.classList.add("flex", "centered", "outlined", "donor-weight");

    let donor_name_h2 = document.createElement('h2');
    donor_name_h2.innerHTML = donor.donor_name;
    donor_weight_div.appendChild(donor_name_h2);

    let donor_weight_input = document.createElement('input');
    donor_weight_input.type = "text";
    donor_weight_input.placeholder = "Lbs.";
    donor_weight_input.size = 4;
    donor_weight_input.value = donor.transaction_weight ?? "";

    donor_weight_input.addEventListener('input', (e) => {
        const matches = donor_weight_input.value.match(/^\d*\.?\d*$/g);
        if (matches == null) {
            donor_weight_input.value = donor.transaction_weight;
        } else {
            donor.transaction_weight = donor_weight_input.value;
        }
    });

    donor_weight_div.appendChild(donor_weight_input);

    return donor_weight_div;
}

let constructItemDOMElement = (item) => {
    
    let item_div = document.createElement('div');

    item_div.classList.add("flex", "row", "even", "nowrap", "outlined", "item", "stretch");

    let info_div = document.createElement('div');
    let name_h2 = document.createElement('h2');
    name_h2.innerHTML = item.item_name;
    let donor_h2 = document.createElement('h2');
    donor_h2.innerHTML = item.donor;

    info_div.classList.add("flex", "column", "even");

    info_div.appendChild(name_h2);
    info_div.appendChild(donor_h2);

    let quantity_div = document.createElement('div');
    let increment_button = document.createElement('button');
    increment_button.innerHTML = '+';
    increment_button.classList.add("small", "flex", "centered");
    let quantity_h2 = document.createElement('h2');
    quantity_h2.classList.add("count");
    quantity_h2.innerHTML = item.transaction_quantity;
    let decrement_button = document.createElement('button');
    decrement_button.classList.add("small", "flex", "centered");
    decrement_button.innerHTML = '-';
    
    increment_button.addEventListener('click', (e) => {
        item.transaction_quantity+=1;
        update_total_points_display();
        drawItems();
    });
    
    decrement_button.addEventListener('click', (e) => {
        item.transaction_quantity-=1;
        update_total_points_display();
        if (item.transaction_quantity == 0) {
            items = items.filter(item => item.transaction_quantity > 0);
            const item_donors = items.map(getProp("donor"));
            donors = donors.filter(donor => item_donors.includes(donor.donor_name));
        }
        drawItems();
        drawDonorWeights();
    });

    quantity_div.classList.add("flex", "column", "even");

    quantity_div.appendChild(increment_button);
    quantity_div.appendChild(quantity_h2);
    quantity_div.appendChild(decrement_button);

    let points_div = document.createElement('div');
    let points_h1 = document.createElement('h1');
    points_h1.innerHTML = item.item_points;
    points_h1.classList.add("count");

    points_div.classList.add("flex", "column", "centered");

    points_div.appendChild(points_h1);

    item_div.appendChild(info_div);
    item_div.appendChild(quantity_div);
    item_div.appendChild(points_div);

    return item_div;
}

let onScanSuccess = async (barcode) => {
    barcode = barcode.match(/\d{7}/)[0];
    console.log("Scanned ", barcode);

    const barcodes = items.map(getProp("item_barcode"));
    if (!barcodes.includes(barcode)) {

        let item_res = await fetch(`/api/item/barcode/${barcode}`);
        let item = await item_res.json();
        let donor_res = await fetch(`/api/donor/${item.donor_id}`);
        let donor = await donor_res.json();

        item.donor = donor.donor_name;
        item.transaction_quantity = 1;

        items.push(item);
        update_total_points_display();
        drawItems();

        const donor_names = donors.map(getProp("donor_name"))
        if (!donor_names.includes(donor.donor_name)) {
            donor.transaction_weight = "";
            donors.push(donor)
        }
        drawDonorWeights();
    }
}

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
        items_div.classList.add("bad-flash");
        setTimeout(() => {
            items_div.classList.remove("bad-flash");
        }, 1000);
        return false;
    }

    for (const donor of donors) {
        if (donor.transaction_weight == "") {
            donors_div.classList.add("bad-flash");
            setTimeout(() => {
                donors_div.classList.remove("bad-flash");
            }, 1000);
            return false;
        }
    }

    const customer_id = student_id_input.value;
    if (customer_id == "") {
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

    const customer_id = student_id_input.value;
    const manager_id = getCookie("user_id");

    const res = await fetch('/api/transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            customer_id: customer_id,
            manager_id: manager_id
        })
    });

    const res_json = await res.json()
    const transaction_id = res_json.transaction_id;

    for (const item of items) {
        const res = await fetch('/api/transaction/item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_id: item.item_id,
                transaction_id: transaction_id,
                transaction_quantity: item.transaction_quantity
            })
        });
    }

    for (const donor of donors) {
        const res = await fetch('/api/transaction/weight', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                donor_id: donor.donor_id,
                transaction_id: transaction_id,
                weight: donor.transaction_weight
            })
        });
    }

    window.location.href = "/";
});