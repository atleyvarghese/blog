# Blog
An sample project to manage Blog using API build using Django, GraphQL.

## Setup of development environment

Clone this project:

    $ git clone git@github.com:atleyvarghese/blog.git

It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ source env/local.env
$ python manage.py migrate
```


## Populating sample data
Use the following commands to populating sample data.

    $ python manage.py loaddata fixtures/*


## Starting app

    $ python manage.py runserver

The app will be served by django **runserver**

Access it through **http://localhost:8000**
