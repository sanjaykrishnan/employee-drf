# employee-drf
A sample DRF project


Use employee.csv as a reference csv file.

As mentioned in the problem, the file cannot have more than 5 columns and can have only 21 rows including the header.

Token authentication has been implemented.

A collection has been created.
https://www.postman.com/collections/06024aa8b6d78b6fcfa3

Register API('register/', method='POST') keys:
username
password
password2
email
first_name
last_name

Login API(url='login/', method='POST') keys:
username
password

response will contain the token, use that as header.

Header for below requests:
Authorization:Token {{token}}

Employee listing(url='api/employees/', method='GET')

Employee CSV update(url='api/employees/bulk-save/', method='POST') keys:
file
