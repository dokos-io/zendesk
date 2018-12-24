### ERPNext to Zendesk

In order to differentiate a customer from a supplier, the application adds a custom field name "Is a supplier".
This custom field is then used as a key to filter customers and suppliers.

#### ERPNext Customer to Zendesk Organization

*Basic Mapping*  

|Source|Target|
|---|---|
|Customer Name|Name|


*Pre and post-processing*  
None.

#### ERPNext Supplier to Zendesk Organization

*Basic Mapping*  

|Source|Target|
|---|---|
|Supplier Name|Name|


*Pre-processing*  
Adds the value "True" to the "Is a supplier" checkbox.


*Post-processing*  
None.

#### ERPNext Contact to Zendesk User

*Basic Mapping*  

|Source|Target|
|---|---|
|Name|Name|
|Email ID|Email|
|Phone|Phone|
|Customer|Organization ID|

*Pre-processing*  
The application fetches the ID of one customer linked to this user (There can only be one linked organization in Zendesk).
It also concatenates the first name and last name of the contact to get a full name (required by Zendesk).

*Post-processing*  
None.