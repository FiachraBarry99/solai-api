# Solai API 

This is a RESTful(ish) API for my Solai project. The project goal is to fully utilise the excess energy generated from my solar panels. 
To do this I will run a number of scripts on a Raspberry Pi which will perform 'services' such as turning on a smart switch, heat water or turn on air conditioning.
This API will be served from the Raspberry Pi over the local network which will allow the client to control which services are running. At the moment the only
service available is one to turn on a smart switch that controls an electric car charger. However, the project is set up to allow further expansion into other services.
Below is a basic system diagram showing the generic architecture of the project:

![System Diagram](/system-diagram.png?raw=true)

This API will allow control and communication between the client and server (Raspberry Pi) regardless of what application used to interact (programmatically, web app, mobile app etc.) This will allow lots of flexibility and make it extremely easy to integrate with new or even third-party applications. I used [flask-RESTX](https://github.com/python-restx/flask-restx) to write the API which automatically generates a Swagger UI to make interacting with the API incrediby easy.

The reason I say RESTful(ish) is that the API is not currently stateless as the list of active/inactive services is stored in the memory of the API, not a database. However, in the future I plan to migrate all the client context from this memory into a database (SQLite, mySQL etc.) which will also run on the Raspberry Pi. Also, currently the client has no control over the conditions which trigger the service (water/air temperature, incoming solar power etc.) These should also be stored in the database and exposed via a separate endpoint of the API.

If you are looking to implement a similar project yourself please don't hesitate to reach out for help or advice I would be more than happy!

## Autocharge
The aim of this service is to use the excess energy generated from the solar panels to charge a electric vehcle. It works by checking the temperature from a Blue Maestro sensor (using an API I wrote myself), checking how much power is coming through the solar panels and then deciding whether to turn on/off a smart switch. The Blue Maestro sensor is placed on our water tank and allows us to heat the water up to a certain temperature before switching on the smart switch. The smart switch has the charger for the car plugged into it.
