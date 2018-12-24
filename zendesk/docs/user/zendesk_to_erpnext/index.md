### Zendesk to ERPNext

In order to differentiate a customer from a supplier, the application adds a custom field name "Is a supplier".
This custom field is then used as a key to filter customers and suppliers.

#### Zendesk Organization to ERPNext Customer

*Basic Mapping*  

|Source|Target|
|---|---|
|Name|Customer Name|

*Pre-processing*  
The application checks for all organizations with the same name but not already linked to a Zendesk Sync ID.
If the organization is a duplicate it throws and error and a manual merge must be performed by an end user.

It uses the default customer group as customer group for any new customer.

*Post-processing*  
None.

#### Zendesk Organization to ERPNext Supplier

*Basic Mapping*  

|Source|Target|
|---|---|
|Name|Supplier Name|

*Pre-processing*  
The application checks for all organizations with the same name but not already linked to a Zendesk Sync ID.
If the organization is a duplicate it throws and error and a manual merge must be performed by an end user.

It uses the default supplier group as supplier group for any new supplier.

*Post-processing*  
None.

#### Zendesk User to ERPNext Contact

*Basic Mapping*  

|Source|Target|
|---|---|
|Firstname|First Name|
|Lastname|Last Name|
|Email|Email ID|
|Phone|Phone|

*Pre-processing*  
The application checks for all contacts with the same name but not already linked to a Zendesk Sync ID.
If the contact is a duplicate it throws and error and a manual merge must be performed by an end user.

The application also splits the full name provided by Zendesk into a first name and a last name.
In order to guarantee the output, it is recommended to follow Zendesk's naming guideline by naming the users as follow:
`last name, first name`.



*Post-processing*  
If the user is linked to an organization in Zendesk, the application finds the corresponding Lead or Customer and link it to the created contact.
Else it creates a new Lead linked to that contact.