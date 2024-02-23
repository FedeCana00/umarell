# Umarell
This is the exam of the Unimore Cloud Systems and Applications course.
<br/><br/>
We want to create an application for managing a new service called ``Umarell as a Service``. In the service you can register construction sites that want to be observed and umarells that are looking for construction sites to watch.
The application has two interfaces:
1. API for construction site and umarell management
2. Web interface for searching for construction sites

The application must be tested for deployment on the GCP platform using the following services:
- **App Engine**
- **Firestore**
- **PubSub**

## Backend API REST
Web API RESTful:
1. **POST** and **GET** to the URL ``/api/v1/umarell/{idumarell}`` to add or retrieve data relating to a umarell
2. **POST** and **GET** to the URL ``/api/v1/cantiere/{idcantiere}`` to add or retrieve data relating to a cantiere
3. **POST** to the URL ``/api/v1/clean`` to delete data in the database
## Web Application
Web page that allows you to query the cantieri site database and
of the umarells. By entering the CAP and selecting cantieri, umarell or both, the list of results found in the database will be returned.
## Pub/Sub
System that implements a notification mechanism that allows umarells to be updated on new cantieri sites. An umarell can register on a topic and receive notifications about new cantieri sites that are added. From the command line it is possible to specify one or more CAP that will be used to filter useful messages.