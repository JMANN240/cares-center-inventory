let items = [];
let donors = [];

Attribute.create_route = '/api/items';
Attribute.read_route = '/api/items';
Attribute.update_route = '/api/items';

const getDonors = async () => {
    donors_res = await fetch('/api/donors');
    donors = await donors_res.json();
    donors = makeKeyValues(donors, 'id', 'name');

    createAttributes();

    await getEntries();
}

const createAttributes = () => {
    
    const name_attribute = new Attribute('name', "Name");
    const points_attribute = new Attribute('points', "Points");
    const quantity_attribute = new Attribute('quantity', "Quantity");
    const donor_attribute = new OptionAttribute('donor_id', "Donor", donors);
    const barcode_attribute = new BarcodeAttribute('barcode', "Barcode");

    name_attribute.display();
    name_attribute.filter();
    name_attribute.parameter();

    points_attribute.display();
    points_attribute.filter();
    points_attribute.parameter();

    quantity_attribute.display();
    quantity_attribute.filter();
    quantity_attribute.parameter();

    donor_attribute.display();
    donor_attribute.filter();
    donor_attribute.parameter();

    barcode_attribute.display();
    barcode_attribute.filter();
}

getDonors();