# Sports API

## Motivation:
The main functional areas are:
- Manage data about sporting events to allow users to place bets.
- Provide API to receive data from external providers and update our system with the latest data about events in real-time.
- Provide access to the support team to allow them to see the most recent data for each event and to query data.


## Approach Taken and Architecture

The application was built using the following components-
- Microservices Architecture - Docker provides efficient containerizing for solutions. A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another. A Docker container image is a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries and settings.
- Framework : Python Flask is a useful framework for developing RESTful APIs. It is lightweight and easy to accomodate into existing applications.
- Database : Postgres provides functionality to use json blob as datatype in columns which is appropriate for our case as we have to store mostly json data. Postgres db is connected to our Flask application through SQLAlchemy.

After deciding on all the technical solution design considerations, code development was started using Agile methodology.
In the first sprint, only the basic functionality was developed. Only after the basic functionality was achieved, the next sprint involved removal of redundant and debug level purpose code. This also involved tailoring the code to achieve any improvements in performance, efficiency and execution speed.


## Code structure and clarity
The code is fully commented and well structurized, defining appropriate Classes and Methods where necessary.


## Performance and Error Handling
The code is optimized and handles the required use cases:-
1. GET : Retrieve match by id.
2. GET : Retrieve football matches ordered by start_time.
3. GET : Retrieve matches filtered by name.
4. POST : NewEvent, A complete new sporting event is being created.
5. POST : UpdateOdds, There is an update for the odds field (all the other fields remain unchanged). Tests :- 
	- Change order of selections passed through POST request-Correct selections are updated.
	- Works for any number of selections.

Error Handling - Basic Error handling is written for Bad Requests. This can be further developed in future sprints gathering and handling the edge cases (try-except blocks).

Performance - Although the code is efficient and optimized, the code for the last Use Case (POST : UpdateOdds) contains selection id matching using FOR loop in the pythonic way. In a future sprint, this can be improved using additional data structures and matching by using Joins or implementing a concept such as Hash Table lookup.


## Testing
Python unittest provides easy functionality to create and run test cases for python RESTful app.
The unit tests in File tests.py are currently being run externally and haven'nt been automated through Docker CI-CD pipeline. To run this, you need all the requirements in the file requirements.txt in the system.


## Future scope
Fully automate the testing process using CI-CD pipelines in Docker applications.


## Execution Instructions
System should have Docker installed.

Directory 'sports_api_Akshay' contains all required files for the docker python RESTful app.
- requirements.txt : contains all the python modules to be installed before the service turns on.
- run.py : Will import app from folder 'sports_api' (__init__.py) and contains run command.
- sports_api/__init__.py : Contains all the app development code.
- test.py : Contains the unit test codes.
- docker-compose.yml : Describes the services to be turned on by the Docker application.
- Dockerfile : Contains all the commands to be called on command line to assemble an image. Use docker-compose build to create an automated build.

Run docker-compose up in the path containing Directory 'sports_api_Akshay' : It should build the docker image if it does not exist and start the services according to the docker-compose.yml file.

Then you can use Postman for testing the URLs and responses or directly view them in browser. (First verify if Table exists in DB and insert few records (NewEvent) through POST method initially)

### URLs:

#### GET
- http://localhost:5000/
- http://localhost:5000/match/8661032861909884225
- http://localhost:5000/match/?sport=football&ordering=startTime
- http://localhost:5000/match/?name=Real%20Madrid%20vs%20Barcelona

#### POST
- http://localhost:5000/add