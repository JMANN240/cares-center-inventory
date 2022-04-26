const manager_search_input = document.querySelector('#manager-search-input');
const student_id_search_input = document.querySelector('#student-id-search-input');
const date_time_search_input = document.querySelector('#date-time-search-input');
const donor_search_input = document.querySelector('#donor-search-input');
const item_search_input = document.querySelector('#item-search-input');

const transactions_div = document.querySelector('#transactions');

let constructTransactionDOMElement = (transaction) => {

    const transaction_div = document.createElement('div');
    transaction_div.classList.add('transaction');

    const info_div = document.createElement('div');
    info_div.classList.add('info')

    const transaction_header = document.createElement('h1');
    transaction_header.innerHTML = `Transaction ${transaction.id}`

    const manager_header = document.createElement('h2');
    manager_header.innerHTML = `Manager: ${transaction.manager.firstname} ${transaction.manager.lastname}`

    const student_header = document.createElement('h2');
    student_header.innerHTML = `Student ID: ${transaction.student_id}`

    const time_header = document.createElement('h2');
    time_header.innerHTML = `Time: ${timestampToFormatted(transaction.time)}`

    info_div.appendChild(transaction_header);
    info_div.appendChild(manager_header);
    info_div.appendChild(student_header);
    info_div.appendChild(time_header);

    transaction_div.appendChild(info_div);

    const records_div = document.createElement('div');
    records_div.classList.add('records')

    let donor_weights = {};

    for (const donor_weight of transaction.weights) {
        donor_weights[donor_weight.donor_id] = donor_weight.weight;
    }

    let donor_records = {};

    for (const transaction_item of transaction.items) {
        if (!Object.keys(donor_records).includes(transaction_item.item.donor.id.toString())) {
            const donor_record = document.createElement('div');
            donor_record.classList.add('donor-record');
            donor_h2 = document.createElement('h2');
            donor_h2.innerHTML = `${transaction_item.item.donor.name}${transaction_item.item.donor.weighs ? `, ${donor_weights[transaction_item.item.donor.id]}lbs` : ''}`
            donor_record.appendChild(donor_h2);
            donor_records[transaction_item.item.donor.id] = donor_record;
        }

        const item_record = document.createElement('div');
        item_record.classList.add('item-record');

        const item_p = document.createElement('p');
        item_p.innerHTML = `${transaction_item.item.name} x${transaction_item.quantity}`

        item_record.appendChild(item_p);

        donor_records[transaction_item.item.donor.id].appendChild(item_record);

        records_div.appendChild(donor_records[transaction_item.item.donor.id]);
    }

    transaction_div.appendChild(records_div);

    return transaction_div;
}

const filterTransactions = (transactions) => {
    const filtered_transactions = transactions.filter((transaction) => {
        const manager_matches = `${transaction.manager.firstname} ${transaction.manager.lastname}`.toLowerCase().includes(manager_search_input.value.toLowerCase()) || manager_search_input.value == "";
        
        const student_id_matches = `${transaction.student_id}`.toLowerCase().includes(student_id_search_input.value.toLowerCase()) || student_id_search_input.value == "";
        
        const date_time_matches = timestampToFormatted(transaction.time).includes(date_time_search_input.value) || date_time_search_input.value == "";
        
        const transaction_donors = transaction.items.map(transaction_item => transaction_item.item.donor.name.toLowerCase())
        let donor_matches = donor_search_input.value == "";
        for (const donor of transaction_donors) {
            if (donor.includes(donor_search_input.value.toLowerCase())) {
                donor_matches = true;
                break;
            }
        }
        
        const transaction_items = transaction.items.map(transaction_item => transaction_item.item.name.toLowerCase())
        console.log(transaction_items);
        let item_matches = item_search_input.value == "";
        for (const item of transaction_items) {
            if (item.includes(item_search_input.value.toLowerCase())) {
                item_matches = true;
                break;
            }
        }
        
        return manager_matches && student_id_matches && date_time_matches && donor_matches && item_matches;
    });
    return filtered_transactions
}

let drawTransactions = () => {
    const filtered_transactions = filterTransactions(transactions);

    console.log(filtered_transactions);

    transactions_div.innerHTML = "";

    for (const transaction of transactions) {
        if (!filtered_transactions.includes(transaction)) continue;
        console.log("drawing");
        console.log(transaction);
        transactions_div.appendChild(constructTransactionDOMElement(transaction));
    }
}

manager_search_input.addEventListener('input', drawTransactions);
student_id_search_input.addEventListener('input', drawTransactions);
date_time_search_input.addEventListener('input', drawTransactions);
donor_search_input.addEventListener('input', drawTransactions);
item_search_input.addEventListener('input', drawTransactions);

let transactions = [];

let init = async () => {
    let transactions_res = await fetch("/api/transactions");
    transactions = await transactions_res.json();

    drawTransactions();
}

init();