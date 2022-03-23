const items_div = document.querySelector('#items');

let cart = [];

let constructItemDOMElement = (item_name, item_donor, item_points) => {
    let item_div = document.createElement('div');

    item_div.classList.add("flex", "row", "even", "nowrap", "outlined", "item");

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
    let quantity_h2 = document.createElement('h2');
    quantity_h2.innerHTML = '1';
    let decrement_button = document.createElement('button');
    decrement_button.innerHTML = '-';

    quantity_div.classList.add("flex", "column", "even");

    quantity_div.appendChild(increment_button);
    quantity_div.appendChild(quantity_h2);
    quantity_div.appendChild(decrement_button);

    let points_div = document.createElement('div');
    let points_h2 = document.createElement('h2');
    points_h2.innerHTML = item_points;

    points_div.classList.add("flex", "column", "centered");

    points_div.appendChild(points_h2);

    item_div.appendChild(info_div);
    item_div.appendChild(quantity_div);
    item_div.appendChild(points_div);

    return item_div;
}

let onScanSuccess = async (decodedText, decodedResult) => {
    console.log("Scanned ", decodedText);
    if (!cart.includes(decodedText)) {
        let item_res = await fetch(`/api/item/${decodedText.substring(0, 7)}`);
        let item = await item_res.json();
        let donor_res = await fetch(`/api/donor/${item.donor_id}`);
        let donor = await donor_res.json();
        cart.push(decodedText);
        items_div.appendChild(constructItemDOMElement(item.item_name, donor.donor_name, item.item_points));
        console.log(cart);
    }
}

//items_div.appendChild(constructItemDOMElement("test", "donor", "1"));

let html5Qrcode = new Html5Qrcode("reader");
html5Qrcode.start({ facingMode: "environment" }, { fps: 10, qrbox: 300 }, onScanSuccess);