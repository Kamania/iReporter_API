[![Coverage Status](https://coveralls.io/repos/github/Kamania/iReporter_API/badge.svg?branch=develop)](https://coveralls.io/github/Kamania/iReporter_API?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/b081bcf0912515a28953/maintainability)](https://codeclimate.com/github/Kamania/iReporter_API/maintainability)
[![Build Status](https://travis-ci.com/Kamania/iReporter_API.svg?branch=develop)](https://travis-ci.com/Kamania/iReporter_API)

# iReporter API Endpoints

```
iReporter is a web app that provides users a platform where they can report corruption cases
 or ask for an intervention.
```

## Tech/ Framework used

```
Python 3
```
```
Flask
```
```
Flask Restful
```

## Features or end points

```
POST records endoint
```
```
GET all record endpoint
```
```
GET specific endpoint
```
```
PATCH specific location endpoint
```
```
PATCH specific comment endpoint
```
```
DELETE specific endpoint
```

```
POST user endoint
```
```
GET user endpoint
```

## Tests
```
To test the code, one needs to install pytest. Using the terminal, cd into the directory/folder containing the project and type pytest.
```
```
The tests so far are as below:
```
| Method | Route | Endpoint Functionality |
| :---         |     :---       |          :--- |
| GET     | /api/v1/records        | View All records     |
| POST     | /api/v1/records        | Add a Record      |
| GET     | /api/v1/records/id       | Retrieve a single record by id     |
| PATCH     | /api/v1/records/id/location'     | Edit a location by ID    |
| PATCH     | /api/v1/records/id/comment'     | Edit a comment by ID    |
| DELETE     | /api/v1/records/id     | delete a record by ID    |

## Installation procedure

Clone the repo

```
git@github.com:Kamania/iReporter_API.git

```
create and activate the virtual environment from terminal

```
$source <env name>/bin/activate

```

Install the project dependencies:
$pip install -r requirements.txt

Run the application via terminal
```
python run.py
```
## Testing
using the pytest from the terminal

```
$pytest
```
## Deployment

```
https://ireporter18.herokuapp.com/

```
# Owner
Kamania