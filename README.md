# Mooli Ordering System
<img src="https://raw.githubusercontent.com/RapDoodle/mooli-ordering-system/master/documents/assets/logo_horizontal_2.png" height="50"/>

## System Requirements

- A Windows / Mac / Linux Server
- MySQL
- Installed Python3

## Screenshots
<img src="https://raw.githubusercontent.com/RapDoodle/mooli-ordering-system/master/documents/screenshots/01.png" height="200"/><img src="https://raw.githubusercontent.com/RapDoodle/mooli-ordering-system/master/documents/screenshots/02.png" height="200"/><img src="https://raw.githubusercontent.com/RapDoodle/mooli-ordering-system/master/documents/screenshots/03.png" height="200"/><br>
<img src="https://raw.githubusercontent.com/RapDoodle/mooli-ordering-system/master/documents/screenshots/04.png" height="200"/>
<br>
<img src="https://raw.githubusercontent.com/RapDoodle/mooli-ordering-system/master/documents/screenshots/05.png" height="200"/>
<br>
<img src="https://raw.githubusercontent.com/RapDoodle/mooli-ordering-system/master/documents/screenshots/06.png" height="200"/>
<br>
<img src="https://raw.githubusercontent.com/RapDoodle/mooli-ordering-system/master/documents/screenshots/07.png" height="200"/>
<br>
<img src="https://raw.githubusercontent.com/RapDoodle/mooli-ordering-system/master/documents/screenshots/08.png" height="200"/>

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
