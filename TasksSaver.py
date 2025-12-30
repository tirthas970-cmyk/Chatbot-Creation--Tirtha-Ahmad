import os
import time
# imports


def deletion():
    time.sleep(90)
    file.__reduce__(the_Input)
deletion()

name_folder = "AIData"
if not os.path.exists(name_folder):  # Fodler Creatio
    os.mkdir(name_folder)
    print("Your folder had been build.")
else:
    print("You are very intelligent. {name_folder} has already been built.")
Jat_bot = True
while Jat_bot :
    for name_folder in __path__:
        print("""What would you like to do today? 
1. Access your documents.
2. Type in a document.
""")
    Choice = input("(1/2)")

    if Choice == "2":
        the_Input = input("Document please:")

        filename = "Document.txt"

        try:
            with open(filename, 'w') as file:
                file.write(the_Input)  # Creates a file that stores everything
            print("This should work!")  # Than this works
            deletion()
        except OSError as e:
            # tells me that it did not work due to an error
            print("This definitly did not work")

    elif Choice == "1":
        print("Document.txt".read())  # Supposed to print the file
    else:
        print("Invalid input")# You prolly did not press 1 or 2

