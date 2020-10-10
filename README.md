# Mooli Ordering System
![](./documents/assets/logo_horizontal_2.png =250x)

## System Requirements

- A Windows / Mac / Linux Server
- MySQL
- Installed Python3

## Screenshots
![](./documents/screenshots/01.png =250x)
![](./documents/screenshots/02.png =250x)
![](./documents/screenshots/03.png =250x)
![](./documents/screenshots/04.png =250x)
![](./documents/screenshots/05.png =250x)
![](./documents/screenshots/06.png =250x)
![](./documents/screenshots/07.png =250x)
![](./documents/screenshots/08.png =250x)

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
