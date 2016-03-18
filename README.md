[![Build Status](https://travis-ci.org/andela-aomondi/bucketlist-api.svg?branch=develop)](https://travis-ci.org/andela-aomondi/bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/andela-aomondi/bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/andela-aomondi/bucketlist-api?branch=develop)
[![Code Health](https://landscape.io/github/andela-aomondi/bucketlist-api/develop/landscape.svg?style=flat)](https://landscape.io/github/andela-aomondi/bucketlist-api/develop)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE)

# Bucketlist API

This is a bucketlist API made using the Python Flask library.

# Features
The API has the following features which can be accessed by registered users.

  1. A user can log in and get an authorization token for any other requests.
    Logging out destroys the users token.
  2. Creating, deleting and updating bucketlists.
  3. Creating, deleting and updating items inside bucketlists.
  4. Viewing bucketlists owned by the logged in user.

# Usage

# Endpoints

| Endpoint             	| Functionality                     	|
|----------------------	|-----------------------------------	|
| POST /auth/login     	| Logs a user in                    	|
| GET /auth/logout     	| Logs a user out                   	|
| POST /bucketlists/   	| Create a new bucket list          	|
| GET /bucketlists/    	| List all the created bucket lists 	|
| GET /bucketlists/    	| Get single bucket lis             	|
| PUT /bucketlists/    	| Update this bucket list           	|
| DELETE /bucketlists/ 	| Delete this single bucket list    	|


# Set up

In the project root folder, follow the following instructions:

  1. Create a virtual environment by running the command `virtualenv venv`.

  2. `cd` into venv and activate it using the command `. bin/activate`.

  3. Back in the root folder, run `pip install -r requirements.txt` to install
  all relevant dependencies.

  4. Run the command `python tasker.py` to create the database with dummy users
  and data.

  5. Run the command `python app.py` to start the server. The application will
  then be live at **http://localhost:5000/**

# Testing

In the project root folder, run command `nosetests`.

# Acknowledgements

This project is built using functionality from the following awesome 3rd party libraries:

  1. [Flask](http://flask.pocoo.org/)
  2. [flask-restful](http://flask-restful-cn.readthedocs.org/en/0.3.4/)
  3. [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
  4. [itsdangerous](http://pythonhosted.org/itsdangerous/)

# License

The MIT License

Copyright (c) 2016 Amos Omondi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
