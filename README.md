# Solai API 

This is a RESTful(ish) API for my Solai project. The project goal is to fully utilise the excess energy generated from my solar panels. 
To do this I will run a number of scripts on a Raspberry Pi which will perform 'services' such as turning on a smart switch, heat water or turn on air conditioning.
This API will be served from the Raspberry Pi over the local network which will allow me to control which services are running. At the moment the only
service available is one to turn on a smart switch that controls an electric car charger. However, the project is set up to allow further expansion into other services.
Below is a basic system diagram showing the generic architecture of the project:

![System Diagram](/system-diagram.png?raw=true)

The reason I say RESTful(ish) is that the API is not currently stateless as the list of active/inactive services is stored in the memory of the API not a database. However, in the future I plan to migrate all the client context from this memory into a database (SQLite, mySQL etc.) which will also run on the Raspberry Pi. Also, currently the client has no control over the conditions which trigger the service (water/air temperature, incoming solar power etc.) These should also be stored in the database and exposed via a separate endpoint of the API.
