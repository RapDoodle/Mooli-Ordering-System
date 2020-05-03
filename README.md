# Mooli Milk Tea Management System
## System Requirements
- A Windows / Mac / Linux Server
- Running MySQL
- Installed Python3
## Instructions
Install dependencies
- Install python (Ubuntu)
  ```bash
  sudo add-apt-repository ppa:jonathonf/python-3.6
  ```
  For other Linux distribution or other operating system, just Google it ;)
- Install required Python packages
  ```bash
  pip install -r requirements.txt
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
  ```
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
