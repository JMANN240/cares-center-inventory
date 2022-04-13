const transactions_div = document.querySelector('#transactions');

let constructTransactionDOMElement = async (transaction) => {

    const transaction_div = document.createElement('div');
    transaction_div.classList.add('transaction');

    const info_div = document.createElement('div');
    info_div.classList.add('info')

    const transaction_header = document.createElement('h1');
    transaction_header.innerHTML = `Transaction ${transaction.transaction_id}`

    const manager_header = document.createElement('h2');
    const manager_res = await fetch(`/api/manager/read/${transaction.manager_id}`);
    const manager = await manager_res.json();
    manager_header.innerHTML = `Manager: ${manager.manager_firstname} ${manager.manager_lastname}`

    const student_header = document.createElement('h2');
    student_header.innerHTML = `Student ID: ${transaction.customer_id}`

    const time_header = document.createElement('h2');
    time_header.innerHTML = `Time: ${timestampToFormatted(transaction.transaction_time)}`

    info_div.appendChild(transaction_header);
    info_div.appendChild(manager_header);
    info_div.appendChild(student_header);
    info_div.appendChild(time_header);

    transaction_div.appendChild(info_div);

    const records_div = document.createElement('div');
    records_div.classList.add('records')

    let transaction_items_res = await fetch(`/api/transaction/items?transaction_id=${transaction.transaction_id}`);
    let transaction_items = await transaction_items_res.json();
    console.log(transaction_items);

    let weights_res = await fetch(`/api/transaction/weights?transaction_id=${transaction.transaction_id}`);
    let weights = await weights_res.json();
    console.log(weights);

    let donor_weights = {};

    for (const donor_weight of weights) {
        donor_weights[donor_weight.donor_id] = donor_weight.weight;
    }

    let donor_records = {};

    for (const transaction_item of transaction_items) {
        let item_res = await fetch(`/api/item/${transaction_item.item_id}`)
        let item = await item_res.json();

        if (!Object.keys(donor_records).includes(item.donor_id.toString())) {
            const donor_record = document.createElement('div');
            donor_record.classList.add('donor-record');
            donor_h2 = document.createElement('h2');
            donor_res = await fetch(`/api/donor/${item.donor_id}`);
            donor = await donor_res.json();
            donor_h2.innerHTML = `${donor.donor_name}, ${donor_weights[donor.donor_id]}lbs`
            donor_record.appendChild(donor_h2);
            donor_records[item.donor_id] = donor_record;
        }

        const item_record = document.createElement('div');
        item_record.classList.add('item-record');

        const item_p = document.createElement('p');
        item_p.innerHTML = `${item.item_name} x${transaction_item.transaction_quantity}`

        item_record.appendChild(item_p);

        donor_records[item.donor_id].appendChild(item_record);

        records_div.appendChild(donor_records[item.donor_id]);

        console.log(item);
    }

    transaction_div.appendChild(records_div);

    return transaction_div;
}

let init = async () => {
    let transactions_res = await fetch("/api/transaction");
    let transactions = await transactions_res.json();
    console.log(transactions);

    for (const transaction of transactions) {
        const transaction_dom_element = await constructTransactionDOMElement(transaction);
        transactions_div.appendChild(transaction_dom_element);
    }
}

init();