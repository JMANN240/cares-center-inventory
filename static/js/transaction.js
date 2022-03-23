const items_div = document.querySelector('#items');
const donors_div = document.querySelector('#donor-weights')

let items = [];

let donors = [];

let constructDonorWeightDOMElement = (donor_name) => {
    let donor_weight_div = document.createElement('div');
    donor_weight_div.classList.add("flex", "centered", "outlined", "donor-weight");

    let donor_name_h2 = document.createElement('h2');
    donor_name_h2.innerHTML = donor_name;
    donor_weight_div.appendChild(donor_name_h2);

    let donor_name_input = document.createElement('input');
    donor_name_input.type = "number";
    donor_name_input.placeholder = "Lbs.";
    donor_weight_div.appendChild(donor_name_input);

    return donor_weight_div;
}

let constructItemDOMElement = (item_name, item_donor, item_points) => {
    let item_div = document.createElement('div');

    item_div.classList.add("flex", "row", "even", "nowrap", "outlined", "item", "stretch");

    let info_div = document.createElement('div');
    let name_h2 = document.createElement('h2');
    name_h2.innerHTML = item_name;
    let donor_h2 = document.createElement('h2');
    donor_h2.innerHTML = item_donor;

    info_div.classList.add("flex", "column", "even");

    info_div.appendChild(name_h2);
    info_div.appendChild(donor_h2);

    let quantity_div = document.createElement('div');
    let increment_button = document.createElement('button');
    increment_button.innerHTML = '+';
    increment_button.classList.add("small", "flex", "centered");
    let quantity_h2 = document.createElement('h2');
    quantity_h2.classList.add("count");
    quantity_h2.innerHTML = '1';
    let decrement_button = document.createElement('button');
    decrement_button.classList.add("small", "flex", "centered");
    decrement_button.innerHTML = '-';
    
    increment_button.addEventListener('click', (e) => {
        let current_quantity = parseInt(quantity_h2.innerHTML);
        let new_quantity = current_quantity+1;
        quantity_h2.innerHTML = new_quantity;
    });
    
    decrement_button.addEventListener('click', (e) => {
        let current_quantity = parseInt(quantity_h2.innerHTML);
        let new_quantity = current_quantity-1;
        if (new_quantity == 0) {
            item_div.remove();
        } else {
            quantity_h2.innerHTML = new_quantity;
        }
    });

    quantity_div.classList.add("flex", "column", "even");

    quantity_div.appendChild(increment_button);
    quantity_div.appendChild(quantity_h2);
    quantity_div.appendChild(decrement_button);

    let points_div = document.createElement('div');
    let points_h1 = document.createElement('h1');
    points_h1.innerHTML = item_points;
    points_h1.classList.add("count");

    points_div.classList.add("flex", "column", "centered");

    points_div.appendChild(points_h1);

    item_div.appendChild(info_div);
    item_div.appendChild(quantity_div);
    item_div.appendChild(points_div);

    return item_div;
}



let onScanSuccess = async (decodedText, decodedResult) => {
    console.log("Scanned ", decodedText);
    if (!items.map(item => item.item_name).includes(decodedText)) {
        let item_res = await fetch(`/api/item/${decodedText.substring(0, 7)}`);
        let item = await item_res.json();
        let donor_res = await fetch(`/api/donor/${item.donor_id}`);
        let donor = await donor_res.json();
        if (!donors.includes(donor.donor_name)) {
            donors.push(donor.donor_name);
        }
        items.push(item);
        items_div.appendChild(constructItemDOMElement(item.item_name, donor.donor_name, item.item_points));
        console.log(cart);
    }
}

items_div.appendChild(constructItemDOMElement("test", "donor", "1"));
items_div.appendChild(constructItemDOMElement("test", "donor", "1"));
items_div.appendChild(constructItemDOMElement("test", "donor", "1"));
items_div.appendChild(constructItemDOMElement("test", "donor", "1"));
items_div.appendChild(constructItemDOMElement("test", "donor", "1"));
items_div.appendChild(constructItemDOMElement("test", "donor", "1"));
items_div.appendChild(constructItemDOMElement("test", "donor", "1"));
items_div.appendChild(constructItemDOMElement("test", "donor", "1"));
donors_div.appendChild(constructDonorWeightDOMElement("Starbucks"));
donors_div.appendChild(constructDonorWeightDOMElement("Starbucks"));
donors_div.appendChild(constructDonorWeightDOMElement("Starbucks"));
donors_div.appendChild(constructDonorWeightDOMElement("Starbucks"));
donors_div.appendChild(constructDonorWeightDOMElement("Starbucks"));

let html5Qrcode = new Html5Qrcode("reader");
html5Qrcode.start({ facingMode: "environment" }, { fps: 10, qrbox: 300 }, onScanSuccess);