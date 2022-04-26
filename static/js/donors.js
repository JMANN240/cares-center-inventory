let donors = [];

Attribute.create_route = '/api/donors';
Attribute.read_route = '/api/donors';
Attribute.update_route = '/api/donors';

const name_attribute = new Attribute('name', "Donor");
const weighs_attribute = new CheckboxAttribute('weighs', "Weighs");

name_attribute.display();
name_attribute.filter();
name_attribute.parameter();

weighs_attribute.display();
weighs_attribute.filter();
weighs_attribute.parameter();

getEntries();