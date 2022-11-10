Organisation of the code :

3 main classes : 
  - wrapper/adapter for DBMs (role : ensure code adaptability even if changes on the level of DBMs)
  - Batch SQL Extractor (role : allow read from web app, define the frequency of querying for changes, call the functionnal methods for getting changes
                        and data, initialise the connection between DBMs and HistDB)
  - DB Connector (role : instantiate the functionnal methods to manipulate the data on the SQL extractor machine and make transparent that the operation are
                  on a remote db ) 

helper DT:
  - classes and data types used in the main three classes to semplify the work
------DESCRIPTION OF THE ARCHITECTURE------------

- DBMs side : the DBMs contains three main elements : the transaction data (the bigger batch of data to handle, the one at the heart of the problem) and the customer table (smallest table, rarely changed/updated).
The class that we implement around this DB is a wrapper. It's role is to allow that even in the event of a change in the code of the DB we ensure that the communication and the data transaction task still functions on our server and web app side. 
It allow us also to implement some CDC policy.

    MAIN METHODS IN THE DBWRAPPER 
      - init: instantiate the adapter, also call dbInit to istantiate the "real" db
      - listener: method that is used to comunicate with the external world, it has the reponsability to recive the call, call the method that process it and return the response
      - executeQuery : method that execute a query on the db and can be used to do some additional operation
      - checkCredential: the idea is to have the possibility to define an access policy in addition to the one of the db
      - getChanges: method that take some parameters and is used to do an incremental ETL
      
BATCH SQL EXTRACTOR : that is the interface that allows a smooth transaction of data between the external DB and the company's Db. It contains the methods to instantiate and handle the connection to the external DB aswell as the method to update the data on the company's side when needed

    MAIN METHODS IN THE EXTRACTOR 
    
    - init : istantiate the SQL Extractor
    - firstUpdate: do the bulk copy (first copy of the data)
    - update : method that is used to do the incremental ETL process
    

WEB APP : This is the side where we need the data handled and displayed to the user. The only method that we need on that side is a read method to get the data from the historical DB. the rest of the data treatment is handled by the web app. 
