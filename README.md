# Python Microservice Service Template

Folder Structure


```
    ├── controllers
    │   ├── __init__.py
    │   └── controller.py - - - ├──> Route internal logic,
    |                           └──> Framework Independent
    |
    ├── validators
    |   ├── __init__.py
    |   └── validators.py - - - ───> Framework/Buisiness related validations
    |
    ├── services
    |   ├── __init__.py
    |   └── services.py - - - - ───> External services usage (client)
    |
    ├── db
    │   ├── __init__.py
    │   ├── db.py - - - - - - - ───> Queries and Data Binding
    │   └── connection.py - - - ───> DB connection manager
    |
    |
    ├── main.py  - - - - - - -  ├──> Framework Usage, 
    |                           ├──> Route & Configuration, 
    |                           └──> Run Server
    |
    ├── requirements.txt - - -  ───> PIP required packages
    ├── Dockerfile - - - - - -  ───> Docker Configuration
    ├── run.sh     - - - - - -  ───> Docker helper script
    ├── conf.json  - - - - - -  ───> Configuration File Model
    └── README.md  - - - - - -  ───> This File
    
```

