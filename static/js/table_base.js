const search_div = document.querySelector('#search');

const entries_div = document.querySelector('#entries');
const entries_table = document.querySelector('#entries-table');

const create_div = document.querySelector('#create');
const create_button = document.querySelector('#create-button');

const footer_div = document.querySelector('#footer');

const back_button = document.querySelector('#back-button');
const apply_button = document.querySelector('#apply-button');



class Attribute {
    static filters = [];
    static displays = [];
    static display_inputs = [];
    static parameters = [];

    static onFilterInput;

    static create_route;
    static update_route;

    static entries;

    constructor(attribute, placeholder = null) {
        this.attribute = attribute;
        this.placeholder = placeholder ?? attribute
    }

    filter() {
        this.filter = this.createFilterInput();
        search_div.appendChild(this.filter);
        Attribute.filters.push(this);
    }

    createFilterInput() {
        const input = document.createElement('input');
        input.type = 'text';
        input.classList.add('medium');
        input.id = `${this.attribute}-search-input`;
        input.placeholder = this.placeholder;
        input.addEventListener('input', Attribute.onInput);
        return input;
    }

    matches(entry) {
        return entry[this.attribute].toString().toLowerCase().includes(this.filter.value.toLowerCase()) || this.filter.value == "";
    }

    display() {
        Attribute.displays.push(this);
    }

    createDisplayInput(entry) {
        const input = document.createElement('input');
        input.type = 'text';
        input.value = entry[this.attribute];
        input.classList.add('medium');
        input.placeholder = this.placeholder;
        input.addEventListener('input', (e) => {
            entry[this.attribute] = input.value;
        });
        return input;
    }

    createDisplayHeader() {
        const th = document.createElement('th');
        th.classList.add('big');
        th.innerHTML = this.placeholder;
        return th;
    }

    parameter() {
        this.parameter = this.createParameterInput();
        create_div.insertBefore(this.parameter, create_div.children[create_div.children.length-1]);
        Attribute.parameters.push(this);
    }

    createParameterInput() {
        const input = document.createElement('input');
        input.type = 'text';
        input.classList.add('medium');
        input.id = `${this.attribute}-create-input`;
        input.placeholder = this.placeholder;
        return input;
    }

    get value() {
        return this.parameter.value;
    }

    clear() {
        this.parameter.value = "";
    }

    static validateDisplays() {
        for (const display of Attribute.display_inputs) {
            if (display.value == "") {
                flash("Missing entry attribute", 5000);
                display.classList.add('bad-flash');
                setTimeout(() => {
                    display.classList.remove('bad-flash');
                }, 1000);
                return false;
            }
        }
        return true;
    }

    static validateParameters() {
        for (const parameter of Attribute.parameters) {
            if (parameter.parameter.value == "") {
                flash("Missing new entry parameter", 5000);
                parameter.parameter.classList.add('bad-flash');
                setTimeout(() => {
                    parameter.parameter.classList.remove('bad-flash');
                }, 1000);
                return false;
            }
        }
        return true;
    }

    static clearParameters() {
        for (const parameter of Attribute.parameters) {
            console.log(parameter);
            parameter.clear();
        }
    }
}

class CheckboxAttribute extends Attribute {
    constructor(attribute, placeholder = null) {
        super(attribute, placeholder);
    }

    filter() {
        this.filter = this.createFilterInput();
        search_div.appendChild(this.filter.div);
        Attribute.filters.push(this);
    }

    createFilterInput() {
        const div = document.createElement('div');
        div.classList.add('flex', 'column', 'centered');

        const header = document.createElement('h1');
        header.classList.add('small');
        header.innerHTML = this.placeholder;

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.classList.add('small');
        input.id = `${this.attribute}-search-input`;
        input.addEventListener('input', Attribute.onInput);

        div.appendChild(header);
        div.appendChild(input);

        return {
            div: div,
            header: header,
            input: input
        };
    }

    matches(entry) {
        return (!this.filter.input.checked) || entry[this.attribute];
    }

    createDisplayInput(entry) {
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = entry[this.attribute];
        input.classList.add('medium');
        input.addEventListener('change', (e) => {
            entry[this.attribute] = input.checked;
        });
        return input;
    }

    parameter() {
        this.parameter = this.createParameterInput();
        create_div.insertBefore(this.parameter.div, create_div.children[create_div.children.length-1]);
        Attribute.parameters.push(this);
    }

    createParameterInput() {
        const div = document.createElement('div');
        div.classList.add('flex', 'column', 'centered');

        const header = document.createElement('h1');
        header.classList.add('small');
        header.innerHTML = this.placeholder;

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.classList.add('small');
        input.id = `${this.attribute}-create-input`;

        div.appendChild(header);
        div.appendChild(input);

        return {
            div: div,
            header: header,
            input: input
        };
    }

    get value() {
        return this.parameter.input.checked;
    }

    clear() {
        this.parameter.input.checked = false;
    }
}

class OptionAttribute extends Attribute {
    constructor(attribute, placeholder = null, options) {
        super(attribute, placeholder);
        this.options = options;
    }

    filter() {
        this.filter = this.createFilterInput();
        search_div.appendChild(this.filter);
        Attribute.filters.push(this);
    }

    matches(entry) {
        return this.options[entry[this.attribute]].toString().toLowerCase().includes(this.filter.value.toLowerCase()) || this.filter.value == "";
    }

    createDisplayInput(entry) {
        const select = document.createElement('select');
        select.classList.add('medium');

        for (const option of Object.keys(this.options)) {
            const select_option = document.createElement('option');
            select_option.value = option;
            select_option.innerHTML = this.options[option];
            select_option.selected = entry[this.attribute] == option;

            select.appendChild(select_option);
        }

        select.addEventListener('change', (e) => {
            entry[this.attribute] = parseInt(select.value);
        });

        return select;
    }

    createParameterInput() {
        const select = document.createElement('select');
        select.classList.add('medium');
        select.id = `${this.attribute}-create-input`;

        for (const option of Object.keys(this.options)) {
            const select_option = document.createElement('option');
            select_option.value = option;
            select_option.innerHTML = this.options[option];

            select.appendChild(select_option);
        }

        return select;
    }
}

class PasswordAttribute extends Attribute {
    constructor(attribute, placeholder = null) {
        super(attribute, placeholder);
    }

    createParameterInput() {
        const input = document.createElement('input');
        input.type = 'password';
        input.classList.add('medium');
        input.id = `${this.attribute}-create-input`;
        input.placeholder = this.placeholder;
        return input;
    }
}

class BarcodeAttribute extends Attribute {
    constructor(attribute, placeholder = null) {
        super(attribute, placeholder);
    }

    createDisplayInput(entry) {
        const image = document.createElement('img');
        image.src = `/api/barcode?data=${entry[this.attribute]}`;
        image.classList.add('medium');
        image.alt = this.placeholder;
        return image;
    }
}

const tdWrap = (element) => {
    const td = document.createElement('td');
    td.classList.add('medium');
    td.appendChild(element);
    return td;
}

const filterEntries = () => {
    const filtered_entries = Attribute.entries.filter((entry) => {
        const matches = Attribute.filters.map((filter) => {
            return filter.matches(entry)
        });
        return matches.every(match => match);
    });
    return filtered_entries
}

const drawEntries = () => {
    while (entries_table.rows.length > 0) {
        entries_table.deleteRow(-1);
    }

    const header_row = entries_table.insertRow(0);
    for (const attribute of Attribute.displays) {
        header_row.appendChild(attribute.createDisplayHeader());
    }

    const filtered_entries = filterEntries(Attribute.entries);
    for (const entry of Attribute.entries) {
        if (!filtered_entries.includes(entry)) continue;
        const row = entries_table.insertRow(-1);
        for (const attribute of Attribute.displays) {
            const display_input = attribute.createDisplayInput(entry);
            Attribute.display_inputs.push(display_input);
            row.appendChild(tdWrap(display_input));
        }
    }
}

const getEntries = async () => {
    const entries_res = await fetch(Attribute.read_route);
    entries = await entries_res.json();
    Attribute.entries = entries;
    drawEntries();
}

const makeKeyValues = (objects, key_key, value_key) => {
    return_object = {};
    for (const object of objects) {
        return_object[object[key_key]] = object[value_key];
    }
    return return_object;
}

create_button.addEventListener('click', async () => {
    if (!Attribute.validateParameters()) return;

    let new_entry = {};
    for (const parameter of Attribute.parameters) {
        new_entry[parameter.attribute] = parameter.value;
    }

    console.log(new_entry);

    const res = await fetch(Attribute.create_route, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(new_entry)
    });

    Attribute.clearParameters();

    await getEntries();
    drawEntries();
});

back_button.addEventListener('click', () => {
    window.location.href = "/";
});

apply_button.addEventListener('click', async () => {
    if (!Attribute.validateDisplays()) return;

    try {
        for (const entry of Attribute.entries) {
            await fetch(Attribute.update_route, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(entry)
            });
        }
        apply_button.classList.add('good-flash');
        setTimeout(() => {
            apply_button.classList.remove('good-flash');
        }, 1000);
    } catch {
        apply_button.classList.add('bad-flash');
        setTimeout(() => {
            apply_button.classList.remove('bad-flash');
        }, 1000);
    }
});

Attribute.onInput = () => {
    drawEntries();
}