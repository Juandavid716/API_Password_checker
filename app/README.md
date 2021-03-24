# Password_distribution

Check how strong a password can be based on the <a href="https://github.com/barak-itkin/PESrank"> PESrank </a> algorithm, and using datasets originated with <a href ="https://github.com/d4ichi/PassGAN"> PassGAN </a>


# How to use

1. Sqlite 3 must be installed
2. Clone the repository 
3. Change variable "name_file" by the .txt file that contains the password dataset
4. execute the commmand: python main.py
5. This will generate a database called test with a series of tables corresponding to the dimensions and a hash (used to update the dataset)
6. Check in console the results