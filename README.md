# Event-Sourcing
This project is a service that implements a rudimentary version of event
sourcing.
The application consists of 3 parts.
1. A REST API server
2. A producer service that can broadcast random events to the API continuously
3. A web UI that can display results as well as submit it's own events

I have used Python and Flask framework for this project.

## Run the project

Install the required dependencies for this project by executing this command 
```bash
pip install -r requirements.txt
```
It has to two python files Api.py and Producer_Service.py which has to be run in two different terminal.
- First run the Api.py file
```bash
python Api.py
```
- Then in different terminal run Producer_Service.py
```bash
python Producer_Service.py
```
# Challenge Instructions:

For this project, your goal is to put together a service that implements a rudimentary version of event
sourcing. You may use whatever languages or frameworks you feel best suites the problem and your skill set.

The application consists of 3 parts.
1. A REST API server
2. A producer service that can broadcast random events to the API continuously
3. A web UI that can display results as well as submit it's own events

## REST API Server.

The REST API server collects and stores event data. The server does not have to persist this data between
restarts of the service - though it may do so if you wish.

The API server should respond to the following routes:

### POST /event

Records a new event on the server. Events should be formatted as JSON objects that take the following form:

```bash
{
"type": "<string type>",
"value": "<int value>"
}
```

Where type is a string value of either INCREMENT or DECREMENT and value is a positive integer.
The server should gracefully handle bad-input cases.

### GET /events

Returns a JSON list of all events the server has received, in the order that they happened

### GET /value

Returns the current value of the system, which can be calculated by performing the actions described by all
historical events. For instance, if the server has received the following three events:

```bash
[
{
type: "INCREMENT",
value: 1
},
{
type: "DECREMENT",
value: 3
},
{
type: "INCREMENT",
value: 5
},
```

Then this endpoint should return a value of: (1 - 3 + 5) = 3

### GET value/:t

Instead of returning the latest value, this endpoint should return the value that the system had after the first **t**
events have happened. 

- If the system has received no events, the value should be 0.

- If **t** is less than 0, the function should raise a 400 series error.

- If **t** is greater than the number of events, the function should just return the "current" value, the same result as calling **/value** without a parameter would have.

For example, assume the server has received the following events:

```bash
const events = [
{
type: "INCREMENT",
value: 1
},
{
type: "DECREMENT",
value: 3
},
{
type: "INCREMENT",
value: 5
},
{
type: "INCREMENT",
value: 2
},
```
Then the following table shows the expected outputs of this endpoint for various values of t

| t | v |
|---|---|
| 0 | 0 |
| 1 | 1 |
| 2 | -2|
| 3 | 3 |
| 4 | 5 |

## Producer Service

This is a very simple service/program, all it should do is continuously POST a random event type and random
value (between 1 and 5) to the **/event** endpoint every **x** ms.

## Client Web UI

Create a simple web UI that allows us to:
1. View all historical events
2. View the current value
3. Add a new event via a form
