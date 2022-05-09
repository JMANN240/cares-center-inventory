let managers = [];

Attribute.create_route = '/api/managers';
Attribute.read_route = '/api/managers';
Attribute.update_route = '/api/managers';

getEntries();

const firstname_attribute = new Attribute('firstname', "First Name");
const lastname_attribute = new Attribute('lastname', "Last Name");
const username_attribute = new Attribute('username', "Username");
const is_active_attribute = new CheckboxAttribute('is_active', "Active");
const is_admin_attribute = new CheckboxAttribute('is_admin', "Admin");
const password_attribute = new PasswordAttribute('password', "Password");

firstname_attribute.display();
firstname_attribute.filter();
firstname_attribute.parameter();

lastname_attribute.display();
lastname_attribute.filter();
lastname_attribute.parameter();

username_attribute.display();
username_attribute.filter();
username_attribute.parameter();

is_active_attribute.display();
is_active_attribute.filter();
is_active_attribute.parameter();

is_admin_attribute.display();
is_admin_attribute.filter();
is_admin_attribute.parameter();

password_attribute.parameter();