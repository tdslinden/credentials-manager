# Credentials Manager

Credentials Manager is a program to store credentials on a MySQL database with a terminal (command prompt) interface.

## Prerequisite 
MySQL must be first installed on the operating system. You can choose to use the default databases for your tables. However, it is recommended to create your own database.

## How To Use It
1. Download this repository
2. Run MySQL
3. Setup the config.py file
    a. Replace all the '<>' with the associated information. E.g. `master_password = <replace_with_your_password_here>` 
4. Run main.py

## Main Commands
`i`: Insert New Credentials 
`u`: Update Existing Credentials
`g`: Get Credentials 
`p`: Generate Password 
`d`: Delete Credentials
`q`: Quit Program
