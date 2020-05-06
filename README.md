# Mooli Milk Tea Management System

## System Requirements

- A Windows / Mac / Linux Server
- MySQL
- Installed Python3

## Current Progress

- Finished all UI design for customer
- A user can add / remove / update categories in the dashboard via http://localhost:8000/admin/dashboard/category (Logged is not required at the stage of development)
- Controllers and models for category, customer, product
- Unit testing on the models and controllers mentioned above via `python test.py`
- Some views for the admin

## Instructions

Install dependencies

- Install python (Ubuntu)

  ```bash
  sudo add-apt-repository ppa:jonathonf/python-3.8
  ```

  For other Linux distribution or other operating system, just Google it ;)

- Install required Python packages

  ```bash
  pip install -r requirements.txt
  ```

  Please be noted that some dependencies may not be installed on Debian and Ubuntu. If an error occurred while installing `bcrypt`, run the following command

  ```bash
  sudo apt-get install build-essential libffi-dev python-dev
  ```

- Install MySQL (Ubuntu)

  ```bash
  sudo apt-get update
  sudo apt-get install mysql-server
  ```

- Configure MySQL (Ubuntu)

  ```bash
  sudo mysql_secure_installation utility
  ```

  For more information, please Google it

- Start MySQL

  ```bash
  sudo systemctl start mysql
  ```

- Setup the software

  ```bash
  python setup.py
  ```

  Follow the instructions to finish the installation.

- Run the application

  ```bash
  python app.py
  ```

## Copyright

MIT License
