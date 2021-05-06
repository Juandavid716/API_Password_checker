# Password_distribution

Check how strong a password can be based on the <a href="https://github.com/barak-itkin/PESrank"> PESrank </a> algorithm, and using datasets originated with <a href ="https://github.com/d4ichi/PassGAN"> PassGAN </a>


# How to use

1. Postgresql must be installed
2. Clone the repository 
3. Change variable "name_file" by the .txt file that contains the password dataset
4. Change the var "PROD" to "DEV" to make changes.
5. configure postgresql connection on "settings.py" with your local database (line 29)
6. Activate virtual enviroment -> Scripts\activate.
7. execute the commmand: python wsgi.py
8. This will generate a database on postgres with a series of tables corresponding to the dimensions and a hash (used to update the dataset)
9. Checks results on console or in the local URL. The result is a message showing the strength of a password.

# Authors

* Juan Bojato
* Giovanni Moreno
* Daniel Donado