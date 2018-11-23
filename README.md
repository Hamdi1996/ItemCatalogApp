# Catalog Application
This application is for Udacity's Full Stack Nanodegree catalog project.

### Technologies used
* [Python](https://www.python.org/) - Programming Language
  * [Flask](http://flask.pocoo.org/) - Python framework
  * [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
* [Vagrant](https://www.vagrantup.com/) - Virtual Machine
* [Git](https://git-scm.com/) - Source code management

### Getting up and running
* Make sure you have Vagrant and Oracle VM Virtualbox installed.
```
# Spin up the VM
vagrant up

# Log into VM
vagrant ssh

# Enter project folder
cd /vagrant

# Setup databse file
python database_setup.py

# Create test items to put into the databse
python createtestitems.py

# Run the catalog application
python project.py
```
* Once the project is running head to [localhost:5000](http://localhost:5000/)

##### Note:
This project is for the Udacity Full Stack Web Development Nanodegree program. The goal of this project was to create a catalog web
application that provides a list of items within a variety of categories. This project integrated third party user registation using OAuth
2.0 users that have accounts could then create, edit, and delete items and categories. This project also uses JSON endpoints to return JSON
data to users that are logged into the site.
# item
